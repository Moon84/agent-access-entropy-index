#!/usr/bin/env python3
"""Add document, notes, read-it-later, and knowledge-base tracking sources."""

from __future__ import annotations

import sqlite3
from datetime import date

from index_store import DB_PATH


TODAY = date.today().isoformat()
SOURCE_BATCH = "knowledge-note-tracking"


FIELDS = [
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


ROWS = [
    {
        "resource_id": "aar-0238",
        "platform_en": "Cubox",
        "platform_zh": "Cubox",
        "product_or_resource": "Cubox CLI",
        "domain_en": "Documents and knowledge bases",
        "domain_zh": "文档与知识库",
        "country_region": "China/Global",
        "resource_formats": "CLI;Skill;SDK/API",
        "source_format": "github_repo",
        "official_cli": "Official Cubox CLI",
        "official_skill": "Cubox CLI includes agent/skill installation guidance",
        "official_mcp": "Official MCP not confirmed",
        "official_sdk_api": "Cubox Open API and API extension",
        "source_url": "https://github.com/OLCUBO/cubox-cli",
        "official_status_en": "Official",
        "official_status_zh": "官方",
        "verification_status": "Confirmed",
        "openness_level": "Free/paid account with API key; user library access requires local credential handling",
        "risk_level": "High",
        "description_en": "Cubox official CLI lets agents save, read, search, and organize a user's Cubox reading memory through local CLI/API-key configuration.",
        "description_zh": "Cubox 官方 CLI 可让 Agent 通过本地 CLI/API Key 配置收藏、阅读、搜索和整理用户的 Cubox 阅读记忆。",
        "sort_order": 238,
    },
    {
        "resource_id": "aar-0239",
        "platform_en": "Cubox",
        "platform_zh": "Cubox",
        "product_or_resource": "Cubox Open API",
        "domain_en": "Documents and knowledge bases",
        "domain_zh": "文档与知识库",
        "country_region": "China/Global",
        "resource_formats": "SDK/API;Data export",
        "source_format": "api_docs",
        "official_cli": "",
        "official_skill": "",
        "official_mcp": "",
        "official_sdk_api": "Open API for webpage and memo collection",
        "source_url": "https://help.cubox.pro/save/89d3/",
        "official_status_en": "Official",
        "official_status_zh": "官方",
        "verification_status": "Confirmed",
        "openness_level": "Account/API extension required; API link is a private credential",
        "risk_level": "High",
        "description_en": "Cubox Open API supports saving webpage URLs and memos through JSON POST workflows; API links are private credentials and should stay local.",
        "description_zh": "Cubox 开放 API 支持通过 JSON POST 收藏网页和备忘；API 链接属于私人凭据，应只在本地保存和使用。",
        "sort_order": 239,
    },
    {
        "resource_id": "aar-0240",
        "platform_en": "Cubox",
        "platform_zh": "Cubox",
        "product_or_resource": "Cubox Official Obsidian Plugin",
        "domain_en": "Documents and knowledge bases",
        "domain_zh": "文档与知识库",
        "country_region": "China/Global",
        "resource_formats": "Plugin;SDK/API",
        "source_format": "github_repo",
        "official_cli": "",
        "official_skill": "",
        "official_mcp": "",
        "official_sdk_api": "Obsidian plugin integration",
        "source_url": "https://github.com/OLCUBO/obsidian-cubox",
        "official_status_en": "Official",
        "official_status_zh": "官方",
        "verification_status": "Confirmed",
        "openness_level": "User account/plugin authorization required",
        "risk_level": "Medium",
        "description_en": "Cubox official Obsidian plugin connects Cubox read-it-later and knowledge capture workflows with Obsidian.",
        "description_zh": "Cubox 官方 Obsidian 插件将 Cubox 稍后读和知识采集流程连接到 Obsidian。",
        "sort_order": 240,
    },
    {
        "resource_id": "aar-0241",
        "platform_en": "Tencent ima.copilot",
        "platform_zh": "腾讯 ima.copilot / ima 知识库",
        "product_or_resource": "ima knowledge-base AI workspace",
        "domain_en": "Documents and knowledge bases",
        "domain_zh": "文档与知识库",
        "country_region": "China",
        "resource_formats": "Plugin;Skill;SDK/API",
        "source_format": "official_web",
        "official_cli": "Official CLI not confirmed",
        "official_skill": "ima skill download and agent-interface page available",
        "official_mcp": "Official MCP not confirmed",
        "official_sdk_api": "Agent interface/API key page requires account access",
        "source_url": "https://ima.qq.com/",
        "official_status_en": "Official web source; API/Skill needs review",
        "official_status_zh": "官方网页来源；API/Skill 待复核",
        "verification_status": "Partially confirmed",
        "openness_level": "Account-based product; public API/agent interface needs review",
        "risk_level": "High",
        "description_en": "Tencent ima.copilot is a knowledge-base-centered AI workspace for search, reading, writing, personal/shared knowledge bases, notes, and multimodal document understanding.",
        "description_zh": "腾讯 ima.copilot 是以知识库为核心的 AI 工作台，覆盖搜索、阅读、写作、个人/共享知识库、笔记和多模态文档解读。",
        "sort_order": 241,
    },
    {
        "resource_id": "aar-0242",
        "platform_en": "Tencent ima.copilot",
        "platform_zh": "腾讯 ima.copilot / ima 知识库",
        "product_or_resource": "ima agent interface and skill download",
        "domain_en": "Documents and knowledge bases",
        "domain_zh": "文档与知识库",
        "country_region": "China",
        "resource_formats": "Skill;SDK/API",
        "source_format": "official_web",
        "official_cli": "",
        "official_skill": "ima skill download page",
        "official_mcp": "Official MCP not confirmed",
        "official_sdk_api": "API key/agent interface page",
        "source_url": "https://ima.qq.com/agent-interface",
        "official_status_en": "Official web source; needs review",
        "official_status_zh": "官方网页来源；待复核",
        "verification_status": "Needs review",
        "openness_level": "Account/API key required; public documentation is limited",
        "risk_level": "High",
        "description_en": "ima agent-interface page exposes a skill download and API key entry point, but public API/CLI/MCP details need further review.",
        "description_zh": "ima agent-interface 页面提供 Skill 下载和 API Key 入口，但公开 API/CLI/MCP 细节仍需继续复核。",
        "sort_order": 242,
    },
    {
        "resource_id": "aar-0243",
        "platform_en": "Tencent ima.copilot",
        "platform_zh": "腾讯 ima.copilot / ima 知识库",
        "product_or_resource": "ima knowledge-base browser extension",
        "domain_en": "Documents and knowledge bases",
        "domain_zh": "文档与知识库",
        "country_region": "China",
        "resource_formats": "Plugin",
        "source_format": "official_web",
        "official_cli": "",
        "official_skill": "",
        "official_mcp": "",
        "official_sdk_api": "Browser extension for saving web content to ima knowledge bases",
        "source_url": "https://ima.qq.com/extension-info",
        "official_status_en": "Official",
        "official_status_zh": "官方",
        "verification_status": "Confirmed",
        "openness_level": "Account and browser extension required",
        "risk_level": "Medium",
        "description_en": "ima browser extension saves browsing content into a user's ima knowledge base for search, reading, and writing workflows.",
        "description_zh": "ima 浏览器插件可将浏览内容保存到用户的 ima 知识库，用于搜索、阅读和写作工作流。",
        "sort_order": 243,
    },
    {
        "resource_id": "aar-0244",
        "platform_en": "Notion",
        "platform_zh": "Notion",
        "product_or_resource": "Notion Developer API",
        "domain_en": "Documents and knowledge bases",
        "domain_zh": "文档与知识库",
        "country_region": "United States/Global",
        "resource_formats": "SDK/API;MCP",
        "source_format": "api_docs",
        "official_cli": "",
        "official_skill": "",
        "official_mcp": "Official Notion MCP Server tracked separately",
        "official_sdk_api": "Official Notion API documentation",
        "source_url": "https://developers.notion.com/",
        "official_status_en": "Official",
        "official_status_zh": "官方",
        "verification_status": "Confirmed",
        "openness_level": "Workspace authorization required; public API docs",
        "risk_level": "High",
        "description_en": "Notion Developer API documents integrations for reading and writing pages, databases, comments, users, and other workspace content with explicit workspace authorization.",
        "description_zh": "Notion Developer API 说明如何在工作区授权后读写页面、数据库、评论、用户和其他工作区内容。",
        "sort_order": 244,
    },
    {
        "resource_id": "aar-0245",
        "platform_en": "Obsidian",
        "platform_zh": "Obsidian",
        "product_or_resource": "Obsidian Importer",
        "domain_en": "Documents and knowledge bases",
        "domain_zh": "文档与知识库",
        "country_region": "Global",
        "resource_formats": "Plugin;Data import",
        "source_format": "github_repo",
        "official_cli": "",
        "official_skill": "Obsidian Skills tracked separately",
        "official_mcp": "Official MCP not confirmed",
        "official_sdk_api": "Plugin/import workflow",
        "source_url": "https://github.com/obsidianmd/obsidian-importer",
        "official_status_en": "Official",
        "official_status_zh": "官方",
        "verification_status": "Confirmed",
        "openness_level": "Local-first import; user vault permissions required",
        "risk_level": "Medium",
        "description_en": "Obsidian Importer converts data from apps such as Apple Notes, OneNote, Evernote, Notion, and Google Keep into Markdown files usable in Obsidian.",
        "description_zh": "Obsidian Importer 可将 Apple Notes、OneNote、Evernote、Notion、Google Keep 等应用数据转换为 Obsidian 可使用的 Markdown 文件。",
        "sort_order": 245,
    },
]


ENTITY_OVERRIDES = {
    "ent-cubox": {
        "official_homepage": "https://cubox.pro/",
        "primary_github": "https://github.com/OLCUBO/cubox-cli",
        "primary_docs": "https://help.cubox.pro/ai/agents",
        "commercial_model": "Free/paid account; API key and personal library access must stay local and private",
        "service_description_en": "Cubox provides read-it-later, bookmarking, Open API, official CLI, AI agent skills, and Obsidian integration for personal reading memory workflows.",
        "service_description_zh": "Cubox 提供稍后读、书签、开放 API、官方 CLI、AI Agent Skill 和 Obsidian 集成，用于个人阅读记忆工作流。",
    },
    "ent-tencent-ima-copilot": {
        "official_homepage": "https://ima.qq.com/",
        "primary_github": "",
        "primary_docs": "https://ima.qq.com/agent-interface",
        "commercial_model": "Account-based Tencent AI workspace; API key/skill access requires account and further review",
        "service_description_en": "Tencent ima.copilot provides an AI workspace centered on personal/shared knowledge bases, web capture, notes, multimodal document reading, and agent-interface skill/API entry points.",
        "service_description_zh": "腾讯 ima.copilot 提供以个人/共享知识库为核心的 AI 工作台，支持网页采集、笔记、多模态文档阅读以及 agent-interface Skill/API 入口。",
    },
    "ent-notion": {
        "official_homepage": "https://www.notion.com/",
        "primary_github": "https://github.com/makenotion/notion-mcp-server",
        "primary_docs": "https://developers.notion.com/",
        "commercial_model": "Free/paid SaaS; API and MCP access require workspace authorization",
    },
    "ent-obsidian": {
        "official_homepage": "https://obsidian.md/",
        "primary_github": "https://github.com/obsidianmd/obsidian-importer",
        "primary_docs": "https://docs.obsidian.md/",
        "commercial_model": "Free local-first app with paid sync/publish; plugins operate on local vault permissions",
    },
}


def upsert_data_source(conn: sqlite3.Connection, row: dict[str, object]) -> None:
    values = {field: row.get(field, "") for field in FIELDS}
    values["source_dataset"] = SOURCE_BATCH
    values["checked_at"] = TODAY
    conn.execute("DELETE FROM data_sources WHERE resource_id = ?", (values["resource_id"],))
    conn.execute(
        f"""
        INSERT INTO data_sources ({", ".join(FIELDS)})
        VALUES ({", ".join("?" for _ in FIELDS)})
        """,
        [values[field] for field in FIELDS],
    )


def apply_entity_overrides(conn: sqlite3.Connection) -> None:
    for entity_id, row in ENTITY_OVERRIDES.items():
        conn.execute(
            """
            UPDATE tracked_entities
            SET official_homepage = ?,
                primary_github = ?,
                primary_docs = ?,
                commercial_model = ?,
                service_description_en = COALESCE(NULLIF(?, ''), service_description_en),
                service_description_zh = COALESCE(NULLIF(?, ''), service_description_zh),
                tracking_status = 'needs_review',
                checked_at = ?
            WHERE entity_id = ?
            """,
            (
                row["official_homepage"],
                row["primary_github"],
                row["primary_docs"],
                row["commercial_model"],
                row.get("service_description_en", ""),
                row.get("service_description_zh", ""),
                TODAY,
                entity_id,
            ),
        )


def main() -> int:
    conn = sqlite3.connect(DB_PATH)
    try:
        for row in ROWS:
            upsert_data_source(conn, row)
        conn.commit()
    finally:
        conn.close()

    # New entities are created by export_formats -> sync_entities_from_sources.
    import export_formats

    export_formats.main()

    conn = sqlite3.connect(DB_PATH)
    try:
        apply_entity_overrides(conn)
        conn.commit()
    finally:
        conn.close()

    export_formats.main()
    print(f"upserted {len(ROWS)} knowledge/note tracking rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
