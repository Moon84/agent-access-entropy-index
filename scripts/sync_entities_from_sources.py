#!/usr/bin/env python3
"""Ensure tracked_entities covers every platform/company in data_sources."""

from __future__ import annotations

import json
import re
import sqlite3
import urllib.parse
from collections import Counter, defaultdict
from datetime import date
from typing import Any

import rebuild_index
from index_store import DB_PATH, normalize_url


TRACKED_COLUMNS = rebuild_index.TRACKED_ENTITY_FIELDS
DEFAULT_KEYWORDS = "cli;mcp;sdk;api;rest;graphql;openapi;skill;SKILL.md;plugin;download;dataset;webhook"
EXCLUDE_TERMS = "PHI;PII;patient record;medical records;hospital internal;private dataset;internal only"

TYPE_BY_DOMAIN = [
    ("life science", "Public data source"),
    ("clinical trial", "Public data source"),
    ("regulatory public data", "Public data source"),
    ("bioinformatics", "Professional software"),
    ("financial data", "Data provider"),
    ("crypto", "Software platform"),
    ("cloud", "Software platform"),
    ("developer", "Software platform"),
    ("office", "Software platform"),
    ("social", "Software platform"),
]

SERVICE_BY_DOMAIN = {
    "AI and model platforms": "AI model, developer tooling, and agent workflow services.",
    "AI and agent platforms": "AI agent platform or agent-oriented tooling.",
    "Developer platforms": "Developer platform for code, collaboration, automation, or delivery workflows.",
    "Developer platforms and code hosting": "Code hosting and developer collaboration platform.",
    "Financial data": "Financial data, market data, trading, or research platform.",
    "Financial data and terminals": "Financial data terminal, market data, trading, or research service.",
    "Crypto trading": "Crypto trading, wallet, market data, or blockchain infrastructure service.",
    "Crypto finance": "Crypto finance and blockchain access service.",
    "Cloud, data, and AI": "Cloud, data, database, or AI infrastructure platform.",
    "Cloud and cloud native": "Cloud infrastructure or cloud-native developer platform.",
    "Data platforms and databases": "Database, analytics, or data platform.",
    "Office and collaboration": "Office, collaboration, messaging, or productivity platform.",
    "Office suites": "Office suite, document, spreadsheet, or productivity platform.",
    "Documents and knowledge bases": "Document, knowledge base, or reference management platform.",
    "Social media": "Social media, content, community, or publishing platform.",
    "Data providers": "Public, commercial, or developer-facing data provider.",
}

ZH_SERVICE_BY_DOMAIN = {
    "AI / 模型平台": "AI 模型、开发者工具或 Agent 工作流服务。",
    "AI / Agent": "AI Agent 平台或面向 Agent 的工具服务。",
    "开发者平台": "面向代码、协作、自动化或交付流程的开发者平台。",
    "开发者平台与代码托管": "代码托管和开发者协作平台。",
    "金融数据": "金融数据、行情、交易或投研服务。",
    "金融数据与终端": "金融数据终端、行情、交易或投研服务。",
    "数字货币交易": "数字货币交易、钱包、行情或区块链基础设施服务。",
    "加密金融": "数字货币金融和链上访问服务。",
    "云数据AI": "云、数据、数据库或 AI 基础设施平台。",
    "公有云与云原生": "云基础设施或云原生开发平台。",
    "数据平台与数据库": "数据库、分析或数据平台。",
    "办公协作": "办公、协作、消息或生产力平台。",
    "办公套件": "办公套件、文档、表格或生产力平台。",
    "文档与知识库": "文档、知识库或文献管理平台。",
    "社交媒体": "社交媒体、内容、社区或发布平台。",
    "数据供应商": "公共、商业或开发者可访问的数据供应商。",
}


def slug(value: str) -> str:
    text = value.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:60] or "unknown"


def entity_key(row: dict[str, Any]) -> str:
    raw = (row.get("platform_en") or row.get("platform_zh") or row.get("product_or_resource") or "").strip()
    return rebuild_index.english_name(raw, "") or raw


def entity_id_for(name: str) -> str:
    return f"ent-{slug(name)}"


def split_github(url: str) -> str:
    normalized = normalize_url(url)
    if not normalized.startswith("https://github.com/"):
        return ""
    parts = [part for part in normalized.removeprefix("https://github.com/").split("/") if part]
    if not parts:
        return ""
    if len(parts) == 1:
        return f"https://github.com/{parts[0]}"
    return f"https://github.com/{parts[0]}/{parts[1]}"


def valid_url(url: str) -> bool:
    text = normalize_url(url)
    if not text or text.lower() in {"待补", "todo", "tbd", "n/a", "na"}:
        return False
    if rebuild_index.has_han(text):
        return False
    parsed = urllib.parse.urlparse(text)
    if parsed.netloc == "github.com" and parsed.path.strip("/") == "":
        return False
    return text.startswith("https://") or text.startswith("http://")


def source_type_for_url(url: str) -> str:
    normalized = normalize_url(url)
    parsed = urllib.parse.urlparse(normalized)
    if parsed.netloc != "github.com":
        return "web_page"
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) <= 1:
        return "github_org"
    return "github_repo"


def watch_id(entity_id: str, source_type: str, label: str) -> str:
    return f"{entity_id}-{source_type}-{slug(label)}"[:120]


def watch_keywords(domain_en: str) -> str:
    lower = domain_en.lower()
    extras: list[str] = []
    if "bio" in lower or "life science" in lower:
        extras.extend(["workflow", "blast", "omics"])
    if "financial" in lower:
        extras.extend(["market data", "trading", "terminal"])
    if "crypto" in lower:
        extras.extend(["wallet", "trade", "trading", "mcp"])
    if "office" in lower or "document" in lower:
        extras.extend(["docs", "workspace", "spreadsheet"])
    if "cloud" in lower:
        extras.extend(["cloud", "deploy", "serverless"])
    terms = DEFAULT_KEYWORDS.split(";") + extras
    return ";".join(dict.fromkeys(term for term in terms if term))


def generated_watch_sources(entity: dict[str, str]) -> list[dict[str, str]]:
    sources: list[tuple[str, str, str]] = [
        ("primary_github", entity.get("primary_github", ""), "GitHub"),
        ("primary_docs", entity.get("primary_docs", ""), "Docs"),
        ("official_homepage", entity.get("official_homepage", ""), "Homepage"),
    ]
    watches: list[dict[str, str]] = []
    seen: set[str] = set()
    for source_key, raw_url, label in sources:
        url = normalize_url(raw_url)
        if not valid_url(url) or url in seen:
            continue
        seen.add(url)
        source_type = source_type_for_url(url)
        target = f"{entity.get('entity_name_en') or entity.get('entity_name_zh')} {label}".strip()
        watches.append(
            {
                "watch_id": watch_id(str(entity["entity_id"]), source_type, label),
                "entity_id": str(entity["entity_id"]),
                "domain_zh": str(entity.get("domain_zh", "")),
                "domain_en": str(entity.get("domain_en", "")),
                "target_name": target,
                "source_type": source_type,
                "source_url": url,
                "official_homepage": normalize_url(str(entity.get("official_homepage", ""))) if valid_url(str(entity.get("official_homepage", ""))) else "",
                "keywords": watch_keywords(str(entity.get("domain_en", ""))),
                "exclude_terms": EXCLUDE_TERMS,
                "notes": f"Auto-generated from tracked_entities.{source_key}",
                "checked_at": str(entity.get("checked_at", "")),
            }
        )
    return watches


def merge_watch_sources(existing_json: str, generated: list[dict[str, str]]) -> str:
    try:
        existing = json.loads(existing_json or "[]")
    except json.JSONDecodeError:
        existing = []
    by_url: dict[str, dict[str, str]] = {}
    for item in existing + generated:
        if not isinstance(item, dict):
            continue
        url = normalize_url(str(item.get("source_url", "")))
        if not valid_url(url):
            continue
        normalized = {key: str(value or "") for key, value in item.items()}
        merged = {**normalized, **by_url.get(url, {})} if url in by_url else normalized
        merged["source_url"] = url
        merged["source_type"] = source_type_for_url(url)
        by_url[url] = merged
    return json.dumps(list(by_url.values()), ensure_ascii=False, sort_keys=True)


def first_url(rows: list[dict[str, Any]], predicate) -> str:
    for row in rows:
        url = normalize_url(str(row.get("source_url") or ""))
        if url and predicate(url):
            return url
    return ""


def choose_domain(rows: list[dict[str, Any]], field: str) -> str:
    counts = Counter(str(row.get(field) or "") for row in rows if row.get(field))
    return counts.most_common(1)[0][0] if counts else ""


def choose_country(rows: list[dict[str, Any]]) -> str:
    counts = Counter(str(row.get("country_region") or "") for row in rows if row.get("country_region"))
    return counts.most_common(1)[0][0] if counts else ""


def choose_entity_type(domain_en: str) -> str:
    lower = domain_en.lower()
    for token, entity_type in TYPE_BY_DOMAIN:
        if token in lower:
            return entity_type
    return "Software platform"


def service_description_en(name: str, rows: list[dict[str, Any]]) -> str:
    for row in rows:
        text = str(row.get("description_en") or "").strip()
        if text:
            return text
    domain = choose_domain(rows, "domain_en")
    formats = sorted(
        {
            item
            for row in rows
            for item in str(row.get("resource_formats") or "").split(";")
            if item
        }
    )
    base = SERVICE_BY_DOMAIN.get(domain, "Software, data, or platform service tracked for agent-access resources.")
    if formats:
        return f"{name} provides {base.rstrip('.').lower()}. Indexed access types: {', '.join(formats)}."
    return f"{name} provides {base.rstrip('.').lower()}."


def service_description_zh(name: str, rows: list[dict[str, Any]]) -> str:
    for row in rows:
        text = str(row.get("description_zh") or "").strip()
        if text:
            return text
    domain = choose_domain(rows, "domain_zh")
    formats = sorted(
        {
            item
            for row in rows
            for item in str(row.get("resource_formats") or "").split(";")
            if item
        }
    )
    base = ZH_SERVICE_BY_DOMAIN.get(domain, "被追踪的公开软件、数据或平台服务。")
    if formats:
        return f"{name} 提供{base.rstrip('。')}。已收录可及性类型：{', '.join(formats)}。"
    return f"{name} 提供{base.rstrip('。')}。"


def generated_description(value: str) -> bool:
    text = value or ""
    return " provides " in text and "Indexed access types:" in text


def load_rows(conn: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    return [dict(row) for row in conn.execute(f"SELECT * FROM {table}")]


def ensure_columns(conn: sqlite3.Connection) -> None:
    existing = {row[1] for row in conn.execute("PRAGMA table_info(tracked_entities)")}
    for column in ("service_description_en", "service_description_zh"):
        if column not in existing:
            conn.execute(f"ALTER TABLE tracked_entities ADD COLUMN {column} TEXT DEFAULT ''")


def ensure_schema_fields(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM schema_fields WHERE table_name = 'tracked_entities'")
    for index, field in enumerate(rebuild_index.TRACKED_ENTITY_FIELDS, start=1):
        desc_en, desc_zh = rebuild_index.SCHEMA_DESCRIPTIONS["tracked_entities"][field]
        conn.execute(
            """
            INSERT INTO schema_fields
            (table_name, field_name, data_type, required, description_en, description_zh, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "tracked_entities",
                field,
                "TEXT",
                "yes" if field == "entity_id" else "no",
                desc_en,
                desc_zh,
                index,
            ),
        )


def existing_by_name(entities: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for entity in entities:
        for key in ("entity_name_en", "entity_name_zh"):
            name = str(entity.get(key) or "").strip().lower()
            if name:
                result[name] = entity
    return result


def grouped_sources(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        name = entity_key(row)
        if name:
            groups[name].append(row)
    return groups


def merge_entity(existing: dict[str, Any] | None, name: str, rows: list[dict[str, Any]], today: str) -> dict[str, Any]:
    current = dict(existing or {})
    entity_name_en = rebuild_index.english_name(str(current.get("entity_name_en") or rows[0].get("platform_en") or name), "")
    entity_name_en = entity_name_en or name
    entity_name_zh = str(current.get("entity_name_zh") or rows[0].get("platform_zh") or "")
    domain_en = str(current.get("domain_en") or choose_domain(rows, "domain_en"))
    domain_zh = str(current.get("domain_zh") or choose_domain(rows, "domain_zh"))
    github = str(current.get("primary_github") or first_url(rows, lambda url: "github.com" in url))
    homepage = str(current.get("official_homepage") or first_url(rows, lambda url: "github.com" not in url))
    docs = str(current.get("primary_docs") or "")

    if github and "github.com" in github:
        github = split_github(github)

    entity = {field: str(current.get(field) or "") for field in TRACKED_COLUMNS}
    entity["entity_id"] = entity["entity_id"] or entity_id_for(entity_name_en or entity_name_zh or name)
    entity["entity_name_en"] = entity_name_en
    entity["entity_name_zh"] = entity_name_zh
    entity["entity_type"] = entity["entity_type"] or choose_entity_type(domain_en)
    generated_en = service_description_en(entity_name_en or name, rows)
    generated_zh = service_description_zh(entity_name_zh or entity_name_en or name, rows)
    if not entity["service_description_en"] or generated_description(entity["service_description_en"]):
        entity["service_description_en"] = generated_en
    if not entity["service_description_zh"]:
        entity["service_description_zh"] = generated_zh
    entity["domain_en"] = domain_en
    entity["domain_zh"] = domain_zh
    entity["country_region"] = entity["country_region"] or choose_country(rows)
    entity["official_homepage"] = homepage
    entity["primary_github"] = github
    entity["primary_docs"] = docs
    entity["commercial_model"] = entity["commercial_model"] or "Unknown / needs review"
    entity["tracking_status"] = entity["tracking_status"] or "needs_review"
    entity["index_status"] = "indexed"
    entity["checked_at"] = today
    entity["watch_sources_json"] = merge_watch_sources(entity["watch_sources_json"] or "[]", generated_watch_sources(entity))
    if entity["watch_sources_json"] == "[]":
        entity["tracking_status"] = "needs_source"
    return entity


def replace_entities(conn: sqlite3.Connection, entities: list[dict[str, Any]]) -> None:
    conn.execute("DELETE FROM tracked_entities")
    quoted = ", ".join(f'"{field}"' for field in TRACKED_COLUMNS)
    placeholders = ", ".join("?" for _ in TRACKED_COLUMNS)
    conn.executemany(
        f"INSERT INTO tracked_entities ({quoted}) VALUES ({placeholders})",
        [[entity.get(field, "") for field in TRACKED_COLUMNS] for entity in entities],
    )


def sync_entities(export: bool = True) -> int:
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_columns(conn)
        data_sources = load_rows(conn, "data_sources")
        current_entities = load_rows(conn, "tracked_entities")
        by_name = existing_by_name(current_entities)
        merged: dict[str, dict[str, Any]] = {}

        for name, rows in grouped_sources(data_sources).items():
            existing = by_name.get(name.lower())
            entity = merge_entity(existing, name, rows, today)
            merged[entity["entity_id"]] = entity

        for entity in current_entities:
            entity_id = str(entity.get("entity_id") or "")
            if entity_id and entity_id not in merged:
                kept = {field: str(entity.get(field) or "") for field in TRACKED_COLUMNS}
                if not kept.get("service_description_en"):
                    kept["service_description_en"] = kept.get("notes", "")
                if not kept.get("service_description_zh"):
                    kept["service_description_zh"] = kept.get("notes", "")
                kept["checked_at"] = today
                merged[entity_id] = kept

        ensure_schema_fields(conn)
        replace_entities(conn, sorted(merged.values(), key=lambda row: (row.get("domain_en", ""), row.get("entity_name_en", ""))))
        conn.commit()
    finally:
        conn.close()

    print(f"synced {len(merged)} tracked entities from data_sources")
    if export:
        rebuild_index.export_all()
    return len(merged)


def main() -> int:
    sync_entities(export=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
