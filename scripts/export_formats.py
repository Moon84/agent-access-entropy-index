#!/usr/bin/env python3
"""Export readable files from the primary SQLite index."""

from __future__ import annotations

import rebuild_index


def main() -> None:
    rebuild_index.export_all()
    print("exported readable CSV files and refreshed README statistics")


if __name__ == "__main__":
    main()
