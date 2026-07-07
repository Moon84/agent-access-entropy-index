#!/usr/bin/env python3
"""Update generated resource statistics blocks in both README files."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from index_store import DATA, MANIFEST_PATH, ROOT, data_sources, tracked_entities


START = "<!-- resource-stats:start -->"
END = "<!-- resource-stats:end -->"


def manifest() -> dict[str, object]:
    if not MANIFEST_PATH.exists():
        return {}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def stats() -> dict[str, object]:
    access = data_sources()
    entities = tracked_entities()
    manifest_data = manifest()
    domain_en = Counter(row.get("domain_en", "") for row in access if row.get("domain_en"))
    domain_zh = Counter(row.get("domain_zh", "") for row in access if row.get("domain_zh"))
    platforms = {
        (row.get("platform_en") or row.get("platform_zh") or "").strip().lower()
        for row in access
        if row.get("platform_en") or row.get("platform_zh")
    }
    tracked_names = {
        (row.get("entity_name_en") or row.get("entity_name_zh") or "").strip().lower()
        for row in entities
        if row.get("entity_name_en") or row.get("entity_name_zh")
    }

    return {
        "version": manifest_data.get("version", ""),
        "generated_at": manifest_data.get("generated_at", ""),
        "access_count": len(access),
        "platform_count": len(platforms | tracked_names),
        "domain_count": len(domain_zh or domain_en),
        "domain_top_en": domain_en.most_common(5),
        "domain_top_zh": domain_zh.most_common(5),
        "primary_data": manifest_data.get("primary_data", "data/01-index.sqlite"),
    }


def english_block(values: dict[str, object]) -> str:
    return f"""{START}
## Dataset Snapshot

| Metric | Count |
|---|---:|
| Access resources | {values["access_count"]} |
| Platforms / software | {values["platform_count"]} |
| Industries / domains | {values["domain_count"]} |

Primary data: `{values["primary_data"]}`. Version: `{values["version"]}`.
{END}"""


def chinese_block(values: dict[str, object]) -> str:
    return f"""{START}
## 数据集概览

| 指标 | 数量 |
|---|---:|
| 可及性资源 | {values["access_count"]} |
| 平台 / 软件 | {values["platform_count"]} |
| 行业 / 领域 | {values["domain_count"]} |

主数据：`{values["primary_data"]}`。版本：`{values["version"]}`。
{END}"""


def replace_block(path: Path, block: str, insert_after: str) -> None:
    text = path.read_text(encoding="utf-8")
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        updated = f"{before}\n\n{block}\n\n{after}"
    else:
        if insert_after not in text:
            raise ValueError(f"insert marker not found in {path}: {insert_after}")
        updated = text.replace(insert_after, f"{insert_after}\n\n{block}", 1)
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    values = stats()
    replace_block(ROOT / "README.md", english_block(values), "Information entropy is the first principle of the AI era.")
    replace_block(ROOT / "README.zh-CN.md", chinese_block(values), "信息熵是AI时代的第一性原理")
    print("updated README resource statistics")


if __name__ == "__main__":
    main()
