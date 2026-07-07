#!/usr/bin/env python3
"""Sync tracked entity status from watchlist, candidates, and indexed resources."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ENTITIES_PATH = DATA / "05-tracked-entities.csv"
WATCHLIST_PATH = DATA / "06-tracking-watchlist.csv"
CANDIDATES_DIR = DATA / "09-candidates"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def normalize_url(url: str) -> str:
    text = (url or "").strip().rstrip("/")
    if text.startswith("http://"):
        text = "https://" + text[len("http://") :]
    return text


def latest_candidate_file(prefix: str) -> Path | None:
    files = sorted(CANDIDATES_DIR.glob(f"{prefix}-*.jsonl"))
    return files[-1] if files else None


def indexed_urls() -> set[str]:
    urls: set[str] = set()
    for path in [
        DATA / "01-access-resources.csv",
        DATA / "02-platforms.csv",
        DATA / "03-vendor-openness-matrix.csv",
        DATA / "04-agent-skill-ecosystem.csv",
    ]:
        if not path.exists():
            continue
        _, rows = read_csv(path)
        for row in rows:
            for key in ("source_url", "official_source_url", "github_url"):
                url = normalize_url(row.get(key, ""))
                if url and url not in {"待补", "todo", "tbd", "n/a", "na"}:
                    urls.add(url)
    return urls


def normalize_token(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def entity_index_status(entity: dict[str, str], evidence_urls: set[str], indexed: set[str]) -> str:
    if evidence_urls & indexed:
        return "indexed"
    name = (entity.get("entity_name_en") or entity.get("entity_name_zh") or "").lower()
    if not name:
        return entity.get("index_status", "") or "not_indexed"
    name_token = normalize_token(name)
    for url in indexed:
        if name_token and name_token in normalize_token(url):
            return "indexed"
    return entity.get("index_status", "") or "not_indexed"


def sync_entities(input_path: Path, output_path: Path) -> int:
    fields, entities = read_csv(input_path)
    _, watches = read_csv(WATCHLIST_PATH)
    indexed = indexed_urls()

    watch_count = Counter(watch.get("entity_id", "") for watch in watches)
    evidence_urls_by_entity: dict[str, set[str]] = defaultdict(set)
    for watch in watches:
        entity_id = watch.get("entity_id", "")
        if entity_id:
            for key in ("source_url", "official_homepage"):
                url = normalize_url(watch.get(key, ""))
                if url:
                    evidence_urls_by_entity[entity_id].add(url)

    discovered_file = latest_candidate_file("discovered")
    reviewed_file = latest_candidate_file("reviewed")
    discovered = read_jsonl(discovered_file) if discovered_file else []
    reviewed = read_jsonl(reviewed_file) if reviewed_file else []
    candidate_count = Counter(row.get("entity_id", "") for row in discovered)
    last_discovered = latest_by_entity(discovered, "discovered_at")
    last_reviewed = latest_by_entity(reviewed, "reviewed_at")

    today = date.today().isoformat()
    for entity in entities:
        entity_id = entity.get("entity_id", "")
        entity["watch_count"] = str(watch_count.get(entity_id, 0))
        entity["candidate_count"] = str(candidate_count.get(entity_id, 0))
        if last_discovered.get(entity_id):
            entity["last_discovered_at"] = last_discovered[entity_id]
        if last_reviewed.get(entity_id):
            entity["last_reviewed_at"] = last_reviewed[entity_id]
        for key in ("official_homepage", "primary_github", "primary_docs"):
            url = normalize_url(entity.get(key, ""))
            if url:
                evidence_urls_by_entity[entity_id].add(url)
        entity["index_status"] = entity_index_status(entity, evidence_urls_by_entity.get(entity_id, set()), indexed)
        if not entity.get("tracking_status"):
            entity["tracking_status"] = "active"
        entity["checked_at"] = today

    write_csv(output_path, fields, entities)
    return len(entities)


def latest_by_entity(rows: list[dict[str, Any]], field: str) -> dict[str, str]:
    latest: dict[str, str] = {}
    for row in rows:
        entity_id = str(row.get("entity_id", ""))
        value = str(row.get(field, ""))
        if entity_id and value and value > latest.get(entity_id, ""):
            latest[entity_id] = value
    return latest


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync tracked entity status.")
    parser.add_argument("--input", default=str(ENTITIES_PATH))
    parser.add_argument("--output", default=str(ENTITIES_PATH))
    args = parser.parse_args()

    count = sync_entities(Path(args.input), Path(args.output))
    print(f"synced {count} tracked entities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
