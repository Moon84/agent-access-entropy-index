#!/usr/bin/env python3
"""Print a small summary of the CSV index files."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    platforms = read_csv(ROOT / "data" / "02-platforms.csv")
    access_resources = read_csv(ROOT / "data" / "01-access-resources.csv")
    matrix = read_csv(ROOT / "data" / "03-vendor-openness-matrix.csv")
    ecosystem = read_csv(ROOT / "data" / "04-agent-skill-ecosystem.csv")

    print("Agent Access Entropy Index")
    manifest_path = ROOT / "data" / "08-manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"version: {manifest.get('version')}")
    print(f"01-access-resources.csv: {len(access_resources)} rows")
    print(f"02-platforms.csv: {len(platforms)} rows")
    print(f"03-vendor-openness-matrix.csv: {len(matrix)} rows")
    print(f"04-agent-skill-ecosystem.csv: {len(ecosystem)} rows")
    print()

    print("Unified resource domains")
    for domain, count in Counter(row["domain_en"] for row in access_resources).most_common():
        print(f"- {domain}: {count}")
    print()

    print("Domains")
    for domain, count in Counter(row["domain"] for row in platforms).most_common():
        print(f"- {domain}: {count}")
    print()

    print("Verification status")
    for status, count in Counter(row["verification_status"] for row in platforms).most_common():
        print(f"- {status}: {count}")


if __name__ == "__main__":
    main()
