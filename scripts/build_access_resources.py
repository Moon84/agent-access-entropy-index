#!/usr/bin/env python3
"""Compatibility entrypoint for rebuilding the SQLite index."""

from __future__ import annotations

import rebuild_index


def main() -> None:
    rebuild_index.main()


if __name__ == "__main__":
    main()
