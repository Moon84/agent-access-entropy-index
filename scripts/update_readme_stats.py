#!/usr/bin/env python3
"""Update generated resource statistics blocks in both README files."""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from index_store import DATA, MANIFEST_PATH, ROOT, data_sources, tracked_entities


START = "<!-- resource-stats:start -->"
END = "<!-- resource-stats:end -->"
BAR_WIDTH = 24
TOP_INDUSTRIES = 12


def manifest() -> dict[str, object]:
    if not MANIFEST_PATH.exists():
        return {}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def is_official(row: dict[str, object]) -> bool:
    status = " ".join(
        str(row.get(key, ""))
        for key in ("official_status_en", "official_status_zh", "verification_status")
    ).lower()
    negative_terms = (
        "no official",
        "unconfirmed",
        "pending",
        "partially",
        "partial",
        "quasi",
        "community",
        "未发现",
        "未确认",
        "待复核",
        "部分",
        "准官方",
        "社区",
    )
    if any(term in status for term in negative_terms):
        return False
    official_terms = ("official", "confirmed", "有", "官方", "已确认")
    return any(term in status for term in official_terms)


def stacked_bar(count: int, official_count: int, maximum: int) -> str:
    if maximum <= 0:
        return ""
    filled = min(BAR_WIDTH, round((count / maximum) * BAR_WIDTH))
    if count > 0:
        filled = max(1, filled)
    official_filled = round((official_count / count) * filled) if count else 0
    if official_count > 0:
        official_filled = max(1, official_filled)
    official_filled = min(official_filled, filled)
    unconfirmed_filled = filled - official_filled
    return "█" * official_filled + "▓" * unconfirmed_filled + " " * (BAR_WIDTH - filled)


def percent(value: float) -> str:
    return f"{value:.1%}"


def normalized_entropy(counts: list[int]) -> float:
    total = sum(counts)
    if total <= 0 or len(counts) <= 1:
        return 0
    entropy = 0.0
    for count in counts:
        if count <= 0:
            continue
        probability = count / total
        entropy -= probability * math.log(probability)
    return entropy / math.log(len(counts))


def industry_stats(access: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    zh_labels: dict[str, Counter[str]] = defaultdict(Counter)
    for row in access:
        domain_en = str(row.get("domain_en", "") or "Uncategorized")
        grouped[domain_en].append(row)
        domain_zh = str(row.get("domain_zh", "") or "未分类")
        zh_labels[domain_en][domain_zh] += 1

    rows: list[dict[str, object]] = []
    for domain_en, group in grouped.items():
        official_count = sum(1 for row in group if is_official(row))
        count = len(group)
        rows.append(
            {
                "domain_en": domain_en,
                "domain_zh": zh_labels[domain_en].most_common(1)[0][0],
                "count": count,
                "official_count": official_count,
                "official_ratio": official_count / count if count else 0,
            }
        )
    rows.sort(key=lambda row: (-int(row["count"]), str(row["domain_en"])))
    visible = rows[:TOP_INDUSTRIES]
    maximum = max((int(row["count"]) for row in visible), default=0)
    for row in visible:
        row["bar"] = stacked_bar(
            int(row["count"]),
            int(row["official_count"]),
            maximum,
        )
    return visible


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
    industry_rows = industry_stats(access)
    official_count = sum(1 for row in access if is_official(row))
    official_ratio = official_count / len(access) if access else 0
    industry_entropy = normalized_entropy(list(domain_en.values()))
    access_index = round((0.7 * official_ratio + 0.3 * industry_entropy) * 100, 1)

    return {
        "version": manifest_data.get("version", ""),
        "generated_at": manifest_data.get("generated_at", ""),
        "access_count": len(access),
        "platform_count": len(platforms | tracked_names),
        "domain_count": len(domain_zh or domain_en),
        "domain_top_en": domain_en.most_common(5),
        "domain_top_zh": domain_zh.most_common(5),
        "official_count": official_count,
        "official_ratio": official_ratio,
        "industry_entropy": industry_entropy,
        "access_index": access_index,
        "industry_stats": industry_rows,
        "primary_data": manifest_data.get("primary_data", "data/01-index.sqlite"),
    }


def english_chart(values: dict[str, object]) -> str:
    rows = [
        "| Industry / domain | Resources | Distribution | Official sources | Official share |",
        "|---|---:|---|---:|---:|",
    ]
    for row in values["industry_stats"]:
        rows.append(
            f"| {row['domain_en']} | {row['count']} | `{row['bar']}` | "
            f"{row['official_count']} | {percent(float(row['official_ratio']))} |"
        )
    return "\n".join(rows)


def english_block(values: dict[str, object]) -> str:
    return f"""{START}
## Dataset Snapshot

| Access resources | Platforms / software | Industries / domains | Official source ratio | Access Index |
|---:|---:|---:|---:|---:|
| {values["access_count"]} | {values["platform_count"]} | {values["domain_count"]} | {values["official_count"]} / {values["access_count"]} ({percent(float(values["official_ratio"]))}) | {values["access_index"]} / 100 |

### Industry Coverage

{english_chart(values)}

Access Index = `100 * (0.7 * official_source_ratio + 0.3 * industry_entropy_score)`. The chart shows the top {TOP_INDUSTRIES} industries by resource count; `█` means official sources, `▓` means unconfirmed or non-official sources, and blank space is unfilled length. The industry entropy score is {percent(float(values["industry_entropy"]))} across all industries.

Primary data: `{values["primary_data"]}`. Version: `{values["version"]}`.
{END}"""


def chinese_chart(values: dict[str, object]) -> str:
    rows = [
        "| 行业 / 领域 | 资源数 | 分布 | 官方来源 | 官方占比 |",
        "|---|---:|---|---:|---:|",
    ]
    for row in values["industry_stats"]:
        rows.append(
            f"| {row['domain_zh']} | {row['count']} | `{row['bar']}` | "
            f"{row['official_count']} | {percent(float(row['official_ratio']))} |"
        )
    return "\n".join(rows)


def chinese_block(values: dict[str, object]) -> str:
    return f"""{START}
## 数据集概览

| 可及性资源 | 平台 / 软件 | 行业 / 领域 | 官方来源占比 | Access Index |
|---:|---:|---:|---:|---:|
| {values["access_count"]} | {values["platform_count"]} | {values["domain_count"]} | {values["official_count"]} / {values["access_count"]} ({percent(float(values["official_ratio"]))}) | {values["access_index"]} / 100 |

### 行业覆盖

{chinese_chart(values)}

Access Index = `100 * (0.7 * 官方来源占比 + 0.3 * 行业分布熵得分)`。图表显示资源数最高的 {TOP_INDUSTRIES} 个行业；`█` 表示官方来源，`▓` 表示未确认或非官方来源，空白表示未填充长度。行业分布熵得分按全部行业计算，当前为 {percent(float(values["industry_entropy"]))}。

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
