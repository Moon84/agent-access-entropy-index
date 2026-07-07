#!/usr/bin/env python3
"""Export readable files from the primary SQLite index."""

from __future__ import annotations

import sync_entities_from_sources


def main() -> None:
    sync_entities_from_sources.main()
    print("synced tracked entities, exported readable CSV files, and refreshed README statistics")


if __name__ == "__main__":
    main()
