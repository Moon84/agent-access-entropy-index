# Query Guide

Use [`../data/01-index.sqlite`](../data/01-index.sqlite) as the primary dataset. The CSV files are readable exports for review and GitHub browsing.

## SQLite Examples

List confirmed or likely official MCP resources:

```sql
SELECT platform_en, platform_zh, product_or_resource, source_url
FROM data_sources
WHERE resource_formats LIKE '%MCP%'
  AND official_mcp NOT LIKE '%未%';
```

Search a platform:

```sql
SELECT platform_en, platform_zh, resource_formats, source_url
FROM data_sources
WHERE platform_en LIKE '%Wind%'
   OR platform_zh LIKE '%万得%'
   OR product_or_resource LIKE '%Wind%';
```

Summarize by domain:

```sql
SELECT domain_en, COUNT(*) AS count
FROM data_sources
GROUP BY domain_en
ORDER BY count DESC;
```

Inspect tracked entities and their watch-source count:

```sql
SELECT entity_name_en, domain_en, watch_count, candidate_count, index_status
FROM tracked_entities
ORDER BY domain_en, entity_name_en;
```

## MCP Server

Run the local MCP server over stdio:

```bash
python3 mcp/server.py
```

Available MCP tools:

| Tool | Purpose |
|---|---|
| `search_platform` | Search platforms/resources by keyword. |
| `list_access_resources` | List access resources for a platform. |
| `filter_by_resource_type` | Filter by CLI, Skill, MCP, SDK/API, or Plugin. |
| `list_official_mcp` | List confirmed or likely official MCP resources. |
| `industry_summary` | Summarize counts by domain, resource type, and risk. |
