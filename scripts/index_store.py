#!/usr/bin/env python3
"""Shared SQLite access for the Agent Access Entropy Index."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB_PATH = DATA / "01-index.sqlite"
MANIFEST_PATH = DATA / "04-manifest.json"
CANDIDATES_DIR = DATA / "09-candidates"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def rows(table: str) -> list[dict[str, Any]]:
    with connect() as conn:
        return [dict(row) for row in conn.execute(f"SELECT * FROM {table}")]


def data_sources() -> list[dict[str, Any]]:
    with connect() as conn:
        return [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM data_sources ORDER BY sort_order, platform_en, resource_id"
            )
        ]


def tracked_entities() -> list[dict[str, Any]]:
    with connect() as conn:
        return [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM tracked_entities ORDER BY domain_en, entity_name_en, entity_id"
            )
        ]


def schema_fields() -> list[dict[str, Any]]:
    with connect() as conn:
        return [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM schema_fields ORDER BY table_name, display_order"
            )
        ]


def known_urls() -> set[str]:
    urls: set[str] = set()
    with connect() as conn:
        for row in conn.execute("SELECT source_url FROM data_sources WHERE source_url != ''"):
            url = normalize_url(row["source_url"])
            if url and url.lower() not in {"待补", "todo", "tbd", "n/a", "na"}:
                urls.add(url)
    return urls


def watchlist_rows() -> list[dict[str, str]]:
    watches: list[dict[str, str]] = []
    for entity in tracked_entities():
        raw = entity.get("watch_sources_json") or "[]"
        try:
            sources = json.loads(raw)
        except json.JSONDecodeError:
            sources = []
        for source in sources:
            watch = {key: str(value or "") for key, value in source.items()}
            watch.setdefault("entity_id", str(entity.get("entity_id", "")))
            watch.setdefault("domain_zh", str(entity.get("domain_zh", "")))
            watch.setdefault("domain_en", str(entity.get("domain_en", "")))
            watch.setdefault("official_homepage", str(entity.get("official_homepage", "")))
            watches.append(watch)
    return watches


def normalize_url(url: str) -> str:
    text = (url or "").strip().rstrip("/")
    if text.startswith("http://"):
        text = "https://" + text[len("http://") :]
    return text
