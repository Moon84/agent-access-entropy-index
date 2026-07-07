# Data Dictionary

## `data/01-access-resources.csv`

This is the primary unified table for looking up official-source access resources by platform.

The same records are exported to:

- `data/01-access-resources.jsonl`
- `data/01-access-resources.sqlite`
- `data/07-schema.json`
- `data/08-manifest.json`

Edit `data/01-access-resources.csv` as the source of truth. Regenerate the derived files with:

```bash
python3 scripts/export_formats.py
```

| Field | Description |
|---|---|
| `resource_id` | Stable row identifier for the unified table. |
| `platform_en` | English or romanized platform/vendor name when available. |
| `platform_zh` | Chinese platform/vendor name when available. |
| `product_or_resource` | Product, repository, access resource, or platform-specific resource name. |
| `domain_en` | English domain/category. |
| `domain_zh` | Chinese domain/category. |
| `country_region` | Country or region when known. |
| `access_resource_types` | Normalized resource types, such as CLI, Skill, MCP, SDK/API, Plugin. |
| `official_cli` | Official CLI availability/status from source data. |
| `official_skill` | Official Skill availability/status from source data. |
| `official_mcp` | Official MCP availability/status from source data. |
| `official_sdk_api` | Official SDK/API availability/status from source data. |
| `source_url` | Primary official or evidence URL. |
| `official_status_en` | English official-source status. |
| `official_status_zh` | Chinese official-source status. |
| `verification_status` | Original verification/status value from source data. |
| `openness_level` | Interface/data openness level where available. |
| `risk_level` | Rough risk label inferred from capabilities and category. |
| `description_en` | English short description when available. |
| `description_zh` | Chinese short description when available. |
| `source_dataset` | Source CSV used to build the row. |
| `checked_at` | Last checked date. |

## `data/05-tracked-entities.csv`

This is the base table for tracked companies, platforms, public data resources, and professional software. It links scheduled tracking sources to final database status through `entity_id`.

| Field | Description |
|---|---|
| `entity_id` | Stable entity identifier used by watchlist and candidate records. |
| `entity_name_en` | English or romanized entity name. |
| `entity_name_zh` | Chinese entity name when available. |
| `entity_type` | Entity type, such as public data source, professional software, or software platform. |
| `domain_zh` | Chinese domain/category. |
| `domain_en` | English domain/category. |
| `country_region` | Country or region when known. |
| `official_homepage` | Primary official homepage. |
| `primary_github` | Primary official GitHub organization or repository. |
| `primary_docs` | Primary official documentation or developer page. |
| `commercial_model` | Free, open-source, subscription, commercial, institution-license, or mixed model. |
| `tracking_status` | Tracking lifecycle status such as active, paused, or needs_review. |
| `index_status` | Whether this entity is indexed, not indexed, partial, or pending. |
| `watch_count` | Count of linked watchlist rows. |
| `candidate_count` | Count of latest discovered candidates linked by entity_id. |
| `last_discovered_at` | Latest candidate discovery timestamp. |
| `last_reviewed_at` | Latest candidate review date/timestamp. |
| `last_promoted_at` | Latest date this entity was promoted into a source CSV. |
| `notes` | Short tracking notes. |
| `checked_at` | Last status sync or manual check date. |

## `data/06-tracking-watchlist.csv`

This is the scheduled tracking source list. Each row tracks one official source for one `entity_id`.

| Field | Description |
|---|---|
| `watch_id` | Stable tracking source identifier. |
| `entity_id` | Linked entity in `data/05-tracked-entities.csv`. |
| `domain_zh` | Chinese domain/category used for candidates. |
| `domain_en` | English domain/category used for candidates. |
| `target_name` | Human-readable tracked source name. |
| `source_type` | Source type: github_org, github_user, github_repo, rss, atom, or web_page. |
| `source_url` | Official source URL to poll. |
| `official_homepage` | Official homepage used for double-checking. |
| `keywords` | Semicolon-delimited inclusion filters, such as CLI, MCP, SDK, API, Skill, or SKILL.md. |
| `exclude_terms` | Semicolon-delimited boundary filters for private, patient-level, or internal data. |
| `notes` | Why this source is tracked. |
| `checked_at` | Last manual check date. |

## `data/02-platforms.csv`

| Field | Description |
|---|---|
| `domain` | Broad domain, such as social media, office collaboration, finance data, crypto trading, developer platform, or cloud/data/AI. |
| `platform` | Platform or product name. |
| `official_cli` | Whether an official CLI is available or confirmed. |
| `official_skill` | Whether an official Agent Skill or Skill-like package is available or confirmed. |
| `official_mcp` | Whether an official MCP server/plugin/platform is available or confirmed. |
| `official_source_url` | Primary evidence URL. |
| `verification_status` | Confirmed, partially confirmed, unconfirmed, community, or pending verification. |
| `notes` | Short explanation. |
| `search_keywords` | Keywords used or recommended for reverse lookup. |
| `checked_at` | Last checked date. |

## `data/03-vendor-openness-matrix.csv`

| Field | Description |
|---|---|
| `industry` | Industry category. |
| `company` | Company or vendor. |
| `product_or_platform` | Product, platform, or project name. |
| `country_region` | Country or region if known. |
| `official_cli` | Official CLI status. |
| `official_skill` | Official Skill status. |
| `api_sdk_open` | API/SDK openness level. |
| `data_interface_openness` | Practical openness of the data/interface. |
| `github_url` | GitHub or official source URL. |
| `notes` | Short explanation. |
| `checked_at` | Last checked date. |
