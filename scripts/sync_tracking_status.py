#!/usr/bin/env python3
"""Sync tracked entity status in the primary SQLite index."""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

import rebuild_index
from index_store import CANDIDATES_DIR, DB_PATH, known_urls, normalize_url, tracked_entities


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path or not path.exists():
        return rows
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def latest_candidate_file(prefix: str) -> Path | None:
    files = sorted(CANDIDATES_DIR.glob(f"{prefix}-*.jsonl"))
    return files[-1] if files else None


def normalize_token(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def entity_index_status(entity: dict[str, Any], evidence_urls: set[str], indexed: set[str]) -> str:
    if evidence_urls & indexed:
        return "indexed"
    name = str(entity.get("entity_name_en") or entity.get("entity_name_zh") or "")
    name_token = normalize_token(name)
    for url in indexed:
        if name_token and name_token in normalize_token(url):
            return "indexed"
    return str(entity.get("index_status") or "not_indexed")


def latest_by_entity(rows: list[dict[str, Any]], field: str) -> dict[str, str]:
    latest: dict[str, str] = {}
    for row in rows:
        entity_id = str(row.get("entity_id", ""))
        value = str(row.get(field, ""))
        if entity_id and value and value > latest.get(entity_id, ""):
            latest[entity_id] = value
    return latest


def main() -> int:
    indexed = known_urls()
    discovered = read_jsonl(latest_candidate_file("discovered"))
    reviewed = read_jsonl(latest_candidate_file("reviewed"))
    candidate_count = Counter(row.get("entity_id", "") for row in discovered)
    last_discovered = latest_by_entity(discovered, "discovered_at")
    last_reviewed = latest_by_entity(reviewed, "reviewed_at")

    updates: list[tuple[str, str, str, str, str, str, str, str, str]] = []
    today = date.today().isoformat()
    for entity in tracked_entities():
        entity_id = str(entity.get("entity_id", ""))
        try:
            watch_sources = json.loads(str(entity.get("watch_sources_json") or "[]"))
        except json.JSONDecodeError:
            watch_sources = []
        evidence_urls = {
            normalize_url(str(source.get("source_url", "")))
            for source in watch_sources
            if isinstance(source, dict)
        }
        for key in ("official_homepage", "primary_github", "primary_docs"):
            url = normalize_url(str(entity.get(key, "")))
            if url:
                evidence_urls.add(url)
        updates.append(
            (
                str(len(watch_sources)),
                str(candidate_count.get(entity_id, 0)),
                last_discovered.get(entity_id, str(entity.get("last_discovered_at") or "")),
                last_reviewed.get(entity_id, str(entity.get("last_reviewed_at") or "")),
                entity_index_status(entity, evidence_urls, indexed),
                str(entity.get("tracking_status") or "active"),
                today,
                json.dumps(watch_sources, ensure_ascii=False, sort_keys=True),
                entity_id,
            )
        )

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executemany(
            """
            UPDATE tracked_entities
            SET watch_count = ?,
                candidate_count = ?,
                last_discovered_at = ?,
                last_reviewed_at = ?,
                index_status = ?,
                tracking_status = ?,
                checked_at = ?,
                watch_sources_json = ?
            WHERE entity_id = ?
            """,
            updates,
        )
        conn.commit()
    finally:
        conn.close()

    rebuild_index.export_all()
    print(f"synced {len(updates)} tracked entities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
