#!/usr/bin/env python3
"""Update generated resource statistics blocks in both README files."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
START = "<!-- resource-stats:start -->"
END = "<!-- resource-stats:end -->"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def manifest() -> dict[str, object]:
    path = DATA / "08-manifest.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def stats() -> dict[str, object]:
    access = read_csv(DATA / "01-access-resources.csv")
    platforms = read_csv(DATA / "02-platforms.csv")
    manifest_data = manifest()
    domain_en = Counter(row.get("domain_en", "") for row in access if row.get("domain_en"))
    domain_zh = Counter(row.get("domain_zh", "") for row in access if row.get("domain_zh"))

    return {
        "version": manifest_data.get("version", ""),
        "generated_at": manifest_data.get("generated_at", ""),
        "access_count": len(access),
        "platform_count": len(platforms),
        "domain_count": len(domain_zh or domain_en),
        "domain_top_en": domain_en.most_common(5),
        "domain_top_zh": domain_zh.most_common(5),
    }


def english_block(values: dict[str, object]) -> str:
    top = "\n".join(f"- {name}: {count}" for name, count in values["domain_top_en"])
    return f"""{START}
## Dataset Snapshot

Current coverage:

| Metric | Count |
|---|---:|
| Access resources | {values["access_count"]} |
| Platforms / software | {values["platform_count"]} |
| Industries / domains | {values["domain_count"]} |

Largest domains:

{top}

Dataset version: `{values["version"]}`.
{END}"""


def chinese_block(values: dict[str, object]) -> str:
    top = "\n".join(f"- {name}: {count}" for name, count in values["domain_top_zh"])
    return f"""{START}
## 数据集概览

当前覆盖范围：

| 指标 | 数量 |
|---|---:|
| 访问资源 | {values["access_count"]} |
| 平台 / 软件 | {values["platform_count"]} |
| 行业 / 领域 | {values["domain_count"]} |

收录最多的领域：

{top}

数据集版本：`{values["version"]}`。
{END}"""


def replace_block(path: Path, block: str, insert_after: str) -> None:
    text = path.read_text(encoding="utf-8")
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        updated = f"{before}\n\n{block}\n\n{after}"
    else:
        marker = insert_after
        if marker not in text:
            raise ValueError(f"insert marker not found in {path}: {marker}")
        updated = text.replace(marker, f"{marker}\n\n{block}", 1)
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    values = stats()
    replace_block(ROOT / "README.md", english_block(values), "Candidate outputs are written to `data/09-candidates/`. They are pre-review signals, not verified database entries.")
    replace_block(ROOT / "README.zh-CN.md", chinese_block(values), "候选结果会进入 `data/09-candidates/`。这些是预审信号，不是已确认入库记录。")
    print("updated README resource statistics")


if __name__ == "__main__":
    main()
