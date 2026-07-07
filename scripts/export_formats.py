#!/usr/bin/env python3
"""Export readable files from the primary SQLite index."""

from __future__ import annotations

import sync_entities_from_sources
import sync_tracking_status
import rebuild_index


def main() -> None:
    sync_entities_from_sources.sync_entities(export=False)
    sync_tracking_status.sync_tracking_status(export=False)
    rebuild_index.export_all()
    print("synced tracked entities, exported readable CSV files, and refreshed README statistics")


if __name__ == "__main__":
    main()
