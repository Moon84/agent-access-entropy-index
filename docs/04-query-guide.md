# Query Guide

This project is designed for both human and AI-agent usage.

## Recommended Files

| File | Best for |
|---|---|
| `data/01-access-resources.csv` | Spreadsheet tools, manual review, GitHub preview. |
| `data/01-access-resources.jsonl` | Agent/RAG pipelines, streaming reads, `jq`, line-by-line processing. |
| `data/01-access-resources.sqlite` | Local SQL queries, filtering, aggregation. |
| `data/07-schema.json` | Field validation and tool integration. |
| `data/08-manifest.json` | Version, row count, generated files, and checksums. |

`data/01-access-resources.csv` is the primary dataset. All other files above are derived from it.

Regenerate derived files after editing the CSV:

```bash
python3 scripts/export_formats.py
```

## SQLite Examples

List confirmed or likely official MCP resources:

```sql
SELECT platform_en, platform_zh, product_or_resource, source_url
FROM access_resources
WHERE access_resource_types LIKE '%MCP%'
  AND official_mcp NOT LIKE '%未%';
```

Search a platform:

```sql
SELECT platform_en, platform_zh, access_resource_types, source_url
FROM access_resources
WHERE platform_en LIKE '%Wind%'
   OR platform_zh LIKE '%万得%'
   OR product_or_resource LIKE '%Wind%';
```

Summarize by domain:

```sql
SELECT domain_en, COUNT(*) AS count
FROM access_resources
GROUP BY domain_en
ORDER BY count DESC;
```

## JSONL Examples

Find crypto trading resources:

```bash
jq 'select(.domain_en == "Crypto trading")' data/01-access-resources.jsonl
```

Find official MCP-like resources:

```bash
jq 'select(.access_resource_types | contains("MCP"))' data/01-access-resources.jsonl
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
