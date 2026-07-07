#!/usr/bin/env python3
"""Build and export the three-table SQLite index."""

from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
from datetime import date
from pathlib import Path
from typing import Any

from index_store import DB_PATH, MANIFEST_PATH, ROOT, DATA


DATA_SOURCES_ZH = DATA / "01-data-sources.zh-CN.csv"
DATA_SOURCES_EN = DATA / "01-data-sources.en.csv"
TRACKED_ZH = DATA / "02-tracked-entities.zh-CN.csv"
TRACKED_EN = DATA / "02-tracked-entities.en.csv"
SCHEMA_CSV = DATA / "03-schema.csv"
VERSION_PATH = ROOT / "VERSION"


DATA_SOURCE_FIELDS = [
    "resource_id",
    "platform_en",
    "platform_zh",
    "product_or_resource",
    "domain_en",
    "domain_zh",
    "country_region",
    "resource_formats",
    "source_format",
    "official_cli",
    "official_skill",
    "official_mcp",
    "official_sdk_api",
    "source_url",
    "official_status_en",
    "official_status_zh",
    "verification_status",
    "openness_level",
    "risk_level",
    "description_en",
    "description_zh",
    "source_dataset",
    "checked_at",
    "sort_order",
]

TRACKED_ENTITY_FIELDS = [
    "entity_id",
    "entity_name_en",
    "entity_name_zh",
    "entity_type",
    "domain_zh",
    "domain_en",
    "country_region",
    "official_homepage",
    "primary_github",
    "primary_docs",
    "commercial_model",
    "tracking_status",
    "index_status",
    "watch_count",
    "candidate_count",
    "last_discovered_at",
    "last_reviewed_at",
    "last_promoted_at",
    "notes",
    "checked_at",
    "watch_sources_json",
]

SCHEMA_FIELDS = [
    "table_name",
    "field_name",
    "data_type",
    "required",
    "description_en",
    "description_zh",
    "display_order",
]


SCHEMA_DESCRIPTIONS = {
    "data_sources": {
        "resource_id": ("Stable resource identifier.", "稳定的资源条目 ID。"),
        "platform_en": ("English platform, company, or project name.", "平台、公司或项目英文名。"),
        "platform_zh": ("Chinese platform, company, or project name when available.", "平台、公司或项目中文名。"),
        "product_or_resource": ("Product, data resource, repository, API, SDK, CLI, MCP, or Skill name.", "产品、数据资源、仓库、API、SDK、CLI、MCP 或 Skill 名称。"),
        "domain_en": ("English industry or domain.", "英文行业或领域。"),
        "domain_zh": ("Chinese industry or domain.", "中文行业或领域。"),
        "country_region": ("Country or region when known.", "已知的国家或地区。"),
        "resource_formats": ("Semicolon-delimited access formats such as CLI, MCP, Skill, SDK/API, Plugin, or Data export.", "分号分隔的访问格式，例如 CLI、MCP、Skill、SDK/API、Plugin、Data export。"),
        "source_format": ("Primary evidence/source format, such as GitHub repo, official docs, web page, API docs, or dataset portal.", "主要证据或来源格式，例如 GitHub 仓库、官方文档、网页、API 文档或数据门户。"),
        "official_cli": ("Official CLI status or evidence.", "官方 CLI 状态或证据。"),
        "official_skill": ("Official Agent Skill status or evidence.", "官方 Agent Skill 状态或证据。"),
        "official_mcp": ("Official MCP status or evidence.", "官方 MCP 状态或证据。"),
        "official_sdk_api": ("Official SDK/API status or evidence.", "官方 SDK/API 状态或证据。"),
        "source_url": ("Primary official or evidence URL.", "主要官方来源或证据 URL。"),
        "official_status_en": ("English official-source status.", "英文官方来源状态。"),
        "official_status_zh": ("Chinese official-source status.", "中文官方来源状态。"),
        "verification_status": ("Original verification/status value.", "原始复核或状态值。"),
        "openness_level": ("Interface/data openness level where available.", "接口或数据开放程度。"),
        "risk_level": ("Rough risk label for the access surface.", "访问面的粗略风险标签。"),
        "description_en": ("English notes or description.", "英文说明。"),
        "description_zh": ("Chinese notes or description.", "中文说明。"),
        "source_dataset": ("Original source or import batch.", "原始来源或导入批次。"),
        "checked_at": ("Last checked date.", "最近检查日期。"),
        "sort_order": ("User-facing display priority.", "面向用户的展示排序。"),
    },
    "tracked_entities": {
        "entity_id": ("Stable tracked entity identifier.", "稳定的追踪对象 ID。"),
        "entity_name_en": ("English entity, company, platform, or public data source name.", "追踪对象、公司、平台或公共数据源英文名。"),
        "entity_name_zh": ("Chinese entity name when available.", "追踪对象中文名。"),
        "entity_type": ("Entity type such as public data source, software platform, company, or professional software.", "对象类型，例如公共数据源、软件平台、公司或专业软件。"),
        "domain_zh": ("Chinese domain for tracking.", "追踪对象中文领域。"),
        "domain_en": ("English domain for tracking.", "追踪对象英文领域。"),
        "country_region": ("Country or region when known.", "已知国家或地区。"),
        "official_homepage": ("Official homepage.", "官方网站。"),
        "primary_github": ("Primary official GitHub org/repo.", "主要官方 GitHub 组织或仓库。"),
        "primary_docs": ("Primary official documentation.", "主要官方文档。"),
        "commercial_model": ("Free, paid, mixed, or access model notes.", "免费、收费、混合或访问模式说明。"),
        "tracking_status": ("Tracking status.", "追踪状态。"),
        "index_status": ("Whether this entity already has indexed resources.", "该对象是否已有入库资源。"),
        "watch_count": ("Number of watch sources attached to this entity.", "该对象关联的追踪源数量。"),
        "candidate_count": ("Latest discovered candidate count.", "最近发现的候选数量。"),
        "last_discovered_at": ("Latest discovery timestamp.", "最近发现时间。"),
        "last_reviewed_at": ("Latest review date.", "最近审查日期。"),
        "last_promoted_at": ("Latest database promotion date.", "最近入库日期。"),
        "notes": ("Public non-private tracking notes.", "公开、非隐私追踪说明。"),
        "checked_at": ("Last checked date.", "最近检查日期。"),
        "watch_sources_json": ("JSON array of official websites, RSS/Atom feeds, GitHub sources, docs, or public pages to track.", "官方站点、RSS/Atom、GitHub、文档或公开页面追踪源 JSON 数组。"),
    },
    "schema_fields": {
        "table_name": ("SQLite table name.", "SQLite 表名。"),
        "field_name": ("Field name.", "字段名。"),
        "data_type": ("SQLite data type.", "SQLite 数据类型。"),
        "required": ("Whether the field is required.", "字段是否必填。"),
        "description_en": ("English field description.", "英文字段说明。"),
        "description_zh": ("Chinese field description.", "中文字段说明。"),
        "display_order": ("Display order.", "展示顺序。"),
    },
}


ZH_SOURCE_FIELDS = {
    "resource_id": "资源ID",
    "platform_zh": "平台",
    "product_or_resource": "资源",
    "domain_zh": "领域",
    "country_region": "国家地区",
    "resource_formats": "资源格式",
    "source_format": "来源格式",
    "official_cli": "官方CLI",
    "official_skill": "官方Skill",
    "official_mcp": "官方MCP",
    "official_sdk_api": "官方SDK/API",
    "source_url": "来源URL",
    "official_status_zh": "官方状态",
    "verification_status": "复核状态",
    "openness_level": "开放级别",
    "risk_level": "风险级别",
    "description_zh": "说明",
    "source_dataset": "来源批次",
    "checked_at": "检查日期",
}

EN_SOURCE_FIELDS = {
    "resource_id": "resource_id",
    "platform_en": "platform",
    "product_or_resource": "resource",
    "domain_en": "domain",
    "country_region": "country_region",
    "resource_formats": "resource_formats",
    "source_format": "source_format",
    "official_cli": "official_cli",
    "official_skill": "official_skill",
    "official_mcp": "official_mcp",
    "official_sdk_api": "official_sdk_api",
    "source_url": "source_url",
    "official_status_en": "official_status",
    "verification_status": "verification_status",
    "openness_level": "openness_level",
    "risk_level": "risk_level",
    "description_en": "description",
    "source_dataset": "source_batch",
    "checked_at": "checked_at",
}

ZH_ENTITY_FIELDS = {
    "entity_id": "对象ID",
    "entity_name_zh": "对象",
    "entity_name_en": "英文名",
    "entity_type": "类型",
    "domain_zh": "领域",
    "country_region": "国家地区",
    "official_homepage": "官网",
    "primary_github": "GitHub",
    "primary_docs": "文档",
    "commercial_model": "商业模式",
    "tracking_status": "追踪状态",
    "index_status": "入库状态",
    "watch_count": "追踪源数",
    "candidate_count": "候选数",
    "last_discovered_at": "最近发现",
    "last_reviewed_at": "最近审查",
    "notes": "说明",
    "checked_at": "检查日期",
}

EN_ENTITY_FIELDS = {
    "entity_id": "entity_id",
    "entity_name_en": "entity",
    "entity_name_zh": "chinese_name",
    "entity_type": "entity_type",
    "domain_en": "domain",
    "country_region": "country_region",
    "official_homepage": "homepage",
    "primary_github": "github",
    "primary_docs": "docs",
    "commercial_model": "commercial_model",
    "tracking_status": "tracking_status",
    "index_status": "index_status",
    "watch_count": "watch_sources",
    "candidate_count": "candidates",
    "last_discovered_at": "last_discovered_at",
    "last_reviewed_at": "last_reviewed_at",
    "notes": "notes",
    "checked_at": "checked_at",
}


TEXT_EN = {
    "高": "High",
    "中高": "Medium-high",
    "中": "Medium",
    "低": "Low",
    "官方": "Official",
    "准官方": "Quasi-official",
    "社区": "Community",
    "有": "Available",
    "未确认": "Unconfirmed",
    "未确认官方": "Official source unconfirmed",
    "未确认官方 Skill": "Official Skill unconfirmed",
    "未确认官方 MCP": "Official MCP unconfirmed",
    "未发现": "Not found",
    "未发现官方": "No official source found",
    "未发现官方 CLI": "No official CLI found",
    "未发现官方 Skill": "No official Skill found",
    "未发现官方 MCP": "No official MCP found",
    "未发现官方 Skill/MCP": "No official Skill/MCP found",
    "部分确认": "Partially confirmed",
    "已确认": "Confirmed",
    "已确认 CLI": "Confirmed CLI",
    "已确认 MCP": "Confirmed MCP",
    "已确认 SDK": "Confirmed SDK",
    "已确认 API": "Confirmed API",
    "已确认 Skill": "Confirmed Skill",
    "已确认 CLI/Skill": "Confirmed CLI/Skill",
    "已确认 CLI/MCP": "Confirmed CLI/MCP",
    "已确认 SDK/Skill": "Confirmed SDK/Skill",
    "已确认 Skill/MCP": "Confirmed Skill/MCP",
    "已确认 Skill/MCP 指引": "Confirmed Skill/MCP guidance",
    "待补": "To be added",
}


PHRASE_EN = {
    "有扩展": "Extension available",
    "有 gh": "gh available",
    "有 glab": "glab available",
    "有 Wrangler": "Wrangler available",
    "有 mongosh": "mongosh available",
    "有 hf": "hf available",
    "有本地 CLI": "Local CLI available",
    "Microsoft Skill/MCP 生态": "Microsoft Skill/MCP ecosystem",
    "Skill 内置 CLI 调用": "CLI access through Skill",
    "有 wind-mcp-skill": "wind-mcp-skill available",
    "MCP 平台/Token": "MCP platform/token",
    "未确认 GitHub Skill": "GitHub Skill unconfirmed",
    "有官方 MCP 平台": "Official MCP platform available",
    "AgentKit/Base MCP 生态": "AgentKit/Base MCP ecosystem",
    "有相关 Agent skills": "Related Agent Skills available",
    "有 Base MCP legacy": "Base MCP legacy available",
    "MCP 相关工具": "MCP-related tooling",
    "有 bnbchain-skills": "bnbchain-skills available",
    "有 BNB Chain MCP 指引": "BNB Chain MCP guidance available",
    "awal / AgentKit 工具链": "awal / AgentKit toolchain",
    "有 agentic-wallet-skills": "agentic-wallet-skills available",
    "有 payments-mcp；AgentKit 含 MCP 示例": "payments-mcp available; AgentKit includes MCP examples",
    "有 skills-for-ai-agents-by-CoinMarketCap": "skills-for-ai-agents-by-CoinMarketCap available",
    "Skill 形式支持 MCP Skills": "MCP Skills supported through Skill format",
    "有 @okx_ai/okx-trade-cli": "@okx_ai/okx-trade-cli available",
    "有 okx/agent-skills": "okx/agent-skills available",
    "有 okx/agent-trade-kit": "okx/agent-trade-kit available",
    "CLI/Skill hub 内工具": "Tools in CLI/Skill hub",
    "有 binance-skills-hub": "binance-skills-hub available",
    "未确认官方 MCP；社区 MCP 多": "Official MCP unconfirmed; many community MCP projects",
    "有 kraken-cli": "kraken-cli available",
    "CLI 内置 Agent 场景；未确认独立 Skill 仓库": "Agent workflows built into CLI; standalone Skill repo unconfirmed",
    "CLI 内置 MCP server": "MCP server built into CLI",
    "API/数据平台": "API/data platform",
    "有 hosted/平台 MCP 线索": "Hosted/platform MCP signals found",
    "有 Microsoft Skills": "Microsoft Skills available",
    "有 Microsoft MCP": "Microsoft MCP available",
    "MCP 生态核心方": "Core MCP ecosystem participant",
    "未确认官方 MCP": "Official MCP unconfirmed",
    "有 20+ Agent Skills": "20+ Agent Skills available",
    "基于 MCP metadata/CLI": "MCP metadata/CLI based",
    "Plugin/MCP": "Plugin/MCP",
    "有 gws": "gws available",
    "未确认独立 MCP": "Standalone MCP unconfirmed",
    "未确认官方 CLI": "Official CLI unconfirmed",
    "Plugin/Skill 形态": "Plugin/Skill format",
    "有官方 MCP": "Official MCP available",
    "生态 CLI": "Ecosystem CLI",
    "有 CLI/MCP": "CLI/MCP available",
    "有 Skills": "Skills available",
    "有 MCP": "MCP available",
    "有 hosted MCP / plugin": "Hosted MCP/plugin available",
    "有官方 MCP Skills": "Official MCP Skills available",
    "有 Agent Skill": "Agent Skill available",
    "高，商业授权": "High, commercial license",
    "中高，商业授权": "Medium-high, commercial license",
    "中高，平台授权": "Medium-high, platform license",
    "中高，积分/授权": "Medium-high, points/license",
    "高，账户授权": "High, account authorization",
}


NAME_EN = {
    "米筐 Ricequant": "Ricequant",
    "聚宽 JoinQuant": "JoinQuant",
    "东方财富 Choice": "Eastmoney Choice",
    "同花顺 iFinD": "iFinD",
    "Wind / 万得": "Wind",
    "钉钉 / DingTalk": "DingTalk",
    "Kdocs / 金山文档 / WPS 365": "Kdocs / WPS 365",
    "飞书 / Lark / Feishu": "Lark / Feishu",
    "语雀 / Yuque": "Yuque",
    "Binance / 币安": "Binance",
    "阿里云百炼 Model Studio": "Alibaba Cloud Model Studio",
    "来也 ADP": "Laiye ADP",
    "Choice 金融终端": "Choice financial terminal",
    "小红书": "Xiaohongshu",
    "微信公众号": "WeChat Official Accounts",
    "小红书社区": "Xiaohongshu community",
    "139 个小红书运营技能": "139 Xiaohongshu operations skills",
    "iFinD MCP 平台": "iFinD MCP platform",
}


def has_han(value: object) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in str(value or ""))


def english_name(value: object, fallback: object = "") -> str:
    text = str(value or "").strip()
    if not text:
        return str(fallback or "")
    if text in NAME_EN:
        return NAME_EN[text]
    if "/" in text or "／" in text:
        parts = [part.strip() for part in text.replace("／", "/").split("/")]
        latin = [part for part in parts if part and not has_han(part)]
        if latin:
            return " / ".join(latin)
    if has_han(text):
        fallback_text = str(fallback or "").strip()
        if fallback_text and not has_han(fallback_text):
            return fallback_text
    return text


def english_text(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if text in PHRASE_EN:
        return PHRASE_EN[text]
    if text in TEXT_EN:
        return TEXT_EN[text]
    translated = text
    dictionary = {**TEXT_EN, **PHRASE_EN}
    for source, target in sorted(dictionary.items(), key=lambda item: len(item[0]), reverse=True):
        translated = translated.replace(source, target)
    return "" if has_han(translated) else translated


def english_export_row(row: dict[str, Any], mapping: dict[str, str]) -> dict[str, str]:
    output: dict[str, str] = {}
    for field, label in mapping.items():
        value = row.get(field, "")
        if field in {"platform_en", "entity_name_en", "product_or_resource"}:
            value = english_name(value, row.get("product_or_resource") or row.get("platform_en", ""))
        elif field == "source_url" and has_han(value):
            value = ""
        elif field in {
            "official_cli",
            "official_skill",
            "official_mcp",
            "official_sdk_api",
            "official_status_en",
            "verification_status",
            "openness_level",
            "description_en",
            "notes",
        }:
            value = english_text(value)
        output[label] = str(value or "")
    return output


def schema_rows() -> list[dict[str, Any]]:
    table_fields = {
        "data_sources": DATA_SOURCE_FIELDS,
        "tracked_entities": TRACKED_ENTITY_FIELDS,
        "schema_fields": SCHEMA_FIELDS,
    }
    rows: list[dict[str, Any]] = []
    for table_name, fields in table_fields.items():
        for index, field in enumerate(fields, start=1):
            desc_en, desc_zh = SCHEMA_DESCRIPTIONS[table_name][field]
            rows.append(
                {
                    "table_name": table_name,
                    "field_name": field,
                    "data_type": "INTEGER" if field in {"sort_order", "display_order"} else "TEXT",
                    "required": "yes" if field.endswith("_id") or field in {"table_name", "field_name"} else "no",
                    "description_en": desc_en,
                    "description_zh": desc_zh,
                    "display_order": index,
                }
            )
    return rows


def read_table(table: str) -> list[dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        order = {
            "data_sources": "sort_order, platform_en, resource_id",
            "tracked_entities": "domain_en, entity_name_en, entity_id",
            "schema_fields": "table_name, display_order",
        }[table]
        return [dict(row) for row in conn.execute(f"SELECT * FROM {table} ORDER BY {order}")]
    finally:
        conn.close()


def write_readable_csv(path: Path, mapping: dict[str, str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(mapping.values()), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            if path.name.endswith(".en.csv"):
                writer.writerow(english_export_row(row, mapping))
            else:
                writer.writerow({label: row.get(field, "") for field, label in mapping.items()})


def write_schema_csv(rows: list[dict[str, Any]]) -> None:
    with SCHEMA_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def export_manifest(data_sources: list[dict[str, Any]], entities: list[dict[str, Any]]) -> None:
    version = VERSION_PATH.read_text(encoding="utf-8").strip() if VERSION_PATH.exists() else "0.0.0"
    files = [DB_PATH, DATA_SOURCES_ZH, DATA_SOURCES_EN, TRACKED_ZH, TRACKED_EN, SCHEMA_CSV]
    manifest = {
        "name": "agent-access-entropy-index",
        "version": version,
        "generated_at": date.today().isoformat(),
        "primary_data": "data/01-index.sqlite",
        "tables": ["data_sources", "tracked_entities", "schema_fields"],
        "readable_exports": [
            "data/01-data-sources.zh-CN.csv",
            "data/01-data-sources.en.csv",
            "data/02-tracked-entities.zh-CN.csv",
            "data/02-tracked-entities.en.csv",
            "data/03-schema.csv",
        ],
        "counts": {
            "data_sources": len(data_sources),
            "tracked_entities": len(entities),
            "schema_fields": len(read_table("schema_fields")),
        },
        "files": {
            str(path.relative_to(ROOT)): {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        },
        "sync_rule": "Use data/01-index.sqlite as the primary store. Regenerate readable CSV exports and README statistics with scripts/export_formats.py.",
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def export_all() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"primary SQLite database not found: {DB_PATH}")
    data_sources = read_table("data_sources")
    entities = read_table("tracked_entities")
    schema = read_table("schema_fields")
    write_readable_csv(DATA_SOURCES_ZH, ZH_SOURCE_FIELDS, data_sources)
    write_readable_csv(DATA_SOURCES_EN, EN_SOURCE_FIELDS, data_sources)
    write_readable_csv(TRACKED_ZH, ZH_ENTITY_FIELDS, entities)
    write_readable_csv(TRACKED_EN, EN_ENTITY_FIELDS, entities)
    write_schema_csv(schema)
    export_manifest(data_sources, entities)
    try:
        import update_readme_stats

        update_readme_stats.main()
    except Exception as exc:
        raise RuntimeError("failed to update README resource statistics") from exc


def main() -> None:
    export_all()
    print("exported SQLite primary index and readable CSV files")
    print(f"- {DB_PATH.relative_to(ROOT)}")
    print(f"- {DATA_SOURCES_ZH.relative_to(ROOT)}")
    print(f"- {DATA_SOURCES_EN.relative_to(ROOT)}")
    print(f"- {TRACKED_ZH.relative_to(ROOT)}")
    print(f"- {TRACKED_EN.relative_to(ROOT)}")
    print(f"- {SCHEMA_CSV.relative_to(ROOT)}")
    print(f"- {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
