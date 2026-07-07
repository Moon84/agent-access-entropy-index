#!/usr/bin/env python3
"""Export 01-access-resources.csv to JSONL, SQLite, and 07-schema.json."""

from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CSV_PATH = DATA / "01-access-resources.csv"
JSONL_PATH = DATA / "01-access-resources.jsonl"
SQLITE_PATH = DATA / "01-access-resources.sqlite"
SCHEMA_PATH = DATA / "07-schema.json"
MANIFEST_PATH = DATA / "08-manifest.json"
VERSION_PATH = ROOT / "VERSION"


def read_rows() -> tuple[list[str], list[dict[str, str]]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def export_jsonl(rows: list[dict[str, str]]) -> None:
    with JSONL_PATH.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def export_sqlite(fields: list[str], rows: list[dict[str, str]]) -> None:
    if SQLITE_PATH.exists():
        SQLITE_PATH.unlink()
    conn = sqlite3.connect(SQLITE_PATH)
    try:
        conn.execute(
            "CREATE TABLE access_resources ("
            + ", ".join(f'"{field}" TEXT' for field in fields)
            + ")"
        )
        placeholders = ", ".join("?" for _ in fields)
        quoted_fields = ", ".join(f'"{field}"' for field in fields)
        conn.executemany(
            f"INSERT INTO access_resources ({quoted_fields}) VALUES ({placeholders})",
            [[row.get(field, "") for field in fields] for row in rows],
        )
        conn.execute("CREATE INDEX idx_access_platform_en ON access_resources(platform_en)")
        conn.execute("CREATE INDEX idx_access_platform_zh ON access_resources(platform_zh)")
        conn.execute("CREATE INDEX idx_access_domain_en ON access_resources(domain_en)")
        conn.execute("CREATE INDEX idx_access_domain_zh ON access_resources(domain_zh)")
        conn.execute("CREATE INDEX idx_access_types ON access_resources(access_resource_types)")
        conn.commit()
    finally:
        conn.close()


def export_schema(fields: list[str], rows: list[dict[str, str]]) -> None:
    examples = rows[0] if rows else {}
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Agent Access Entropy Index Access Resource",
        "type": "object",
        "additionalProperties": False,
        "required": fields,
        "properties": {
            field: {
                "type": "string",
                "description": description_for(field),
                "examples": [examples.get(field, "")],
            }
            for field in fields
        },
    }
    SCHEMA_PATH.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def export_manifest(rows: list[dict[str, str]]) -> None:
    version = VERSION_PATH.read_text(encoding="utf-8").strip() if VERSION_PATH.exists() else "0.0.0"
    files = [
        CSV_PATH,
        JSONL_PATH,
        SQLITE_PATH,
        SCHEMA_PATH,
    ]
    manifest = {
        "name": "agent-access-entropy-index",
        "version": version,
        "generated_at": date.today().isoformat(),
        "primary_data": "data/01-access-resources.csv",
        "derived_data": [
            "data/01-access-resources.jsonl",
            "data/01-access-resources.sqlite",
            "data/07-schema.json",
        ],
        "row_count": len(rows),
        "files": {
            str(path.relative_to(ROOT)): {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        },
        "sync_rule": "Edit data/01-access-resources.csv as the primary dataset, then regenerate derived files with scripts/export_formats.py.",
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def description_for(field: str) -> str:
    descriptions = {
        "resource_id": "Stable row identifier.",
        "platform_en": "English or romanized platform/vendor name.",
        "platform_zh": "Chinese platform/vendor name when available.",
        "product_or_resource": "Product, platform, repository, or resource name.",
        "domain_en": "English domain/category.",
        "domain_zh": "Chinese domain/category.",
        "country_region": "Country or region when known.",
        "access_resource_types": "Semicolon-delimited resource types such as CLI, Skill, MCP, SDK/API, Plugin.",
        "official_cli": "Official CLI availability/status.",
        "official_skill": "Official Agent Skill availability/status.",
        "official_mcp": "Official MCP availability/status.",
        "official_sdk_api": "Official SDK/API availability/status.",
        "source_url": "Primary official or evidence URL.",
        "official_status_en": "English official-source status.",
        "official_status_zh": "Chinese official-source status.",
        "verification_status": "Original verification/status value.",
        "openness_level": "Interface/data openness level where available.",
        "risk_level": "Rough risk label inferred from capability and category.",
        "description_en": "English description when available.",
        "description_zh": "Chinese description when available.",
        "source_dataset": "Source CSV used to build the row.",
        "checked_at": "Last checked date.",
    }
    return descriptions.get(field, field)


def main() -> None:
    fields, rows = read_rows()
    export_jsonl(rows)
    export_sqlite(fields, rows)
    export_schema(fields, rows)
    export_manifest(rows)
    try:
        import update_readme_stats

        update_readme_stats.main()
    except Exception as exc:
        raise RuntimeError("failed to update README resource statistics") from exc
    print(f"exported {len(rows)} rows")
    print(f"- {JSONL_PATH.relative_to(ROOT)}")
    print(f"- {SQLITE_PATH.relative_to(ROOT)}")
    print(f"- {SCHEMA_PATH.relative_to(ROOT)}")
    print(f"- {MANIFEST_PATH.relative_to(ROOT)}")
    print("- README.md")
    print("- README.zh-CN.md")


if __name__ == "__main__":
    main()
