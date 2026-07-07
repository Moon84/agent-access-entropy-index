#!/usr/bin/env python3
"""Print a small summary of the SQLite index."""

from __future__ import annotations

import json
from collections import Counter

from index_store import MANIFEST_PATH, data_sources, tracked_entities


def main() -> None:
    resources = data_sources()
    entities = tracked_entities()

    print("Agent Access Entropy Index")
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        print(f"version: {manifest.get('version')}")
    print(f"data_sources: {len(resources)} rows")
    print(f"tracked_entities: {len(entities)} rows")
    print()

    print("Resource domains")
    for domain, count in Counter(row["domain_en"] for row in resources).most_common():
        print(f"- {domain}: {count}")
    print()

    print("Resource formats")
    for item, count in Counter(
        item
        for row in resources
        for item in str(row.get("resource_formats", "")).split(";")
        if item
    ).most_common():
        print(f"- {item}: {count}")
    print()

    print("Tracking domains")
    for domain, count in Counter(row["domain_en"] for row in entities).most_common():
        print(f"- {domain}: {count}")


if __name__ == "__main__":
    main()
