# Data Dictionary

The primary store is [`../data/01-index.sqlite`](../data/01-index.sqlite). CSV files are readable exports only.

## Tables

| Table | Purpose |
|---|---|
| `data_sources` | Access resources, public data resources, platforms, professional software, and official evidence URLs. |
| `tracked_entities` | Companies, platforms, public data sources, and software being tracked. `watch_sources_json` stores the official sites/RSS/GitHub/docs/public pages to poll. |
| `schema_fields` | Field definitions for the three-table SQLite model. |

## Readable Exports

| File | Description |
|---|---|
| [`../data/01-data-sources.en.csv`](../data/01-data-sources.en.csv) | English export for `data_sources`. |
| [`../data/01-data-sources.zh-CN.csv`](../data/01-data-sources.zh-CN.csv) | Chinese export for `data_sources`. |
| [`../data/02-tracked-entities.en.csv`](../data/02-tracked-entities.en.csv) | English export for `tracked_entities`. |
| [`../data/02-tracked-entities.zh-CN.csv`](../data/02-tracked-entities.zh-CN.csv) | Chinese export for `tracked_entities`. |
| [`../data/03-schema.csv`](../data/03-schema.csv) | Export for `schema_fields`. |
| [`../data/04-manifest.json`](../data/04-manifest.json) | Version, table counts, generated files, and checksums. |

## `data_sources`

| Field | Description |
|---|---|
| `resource_id` | Stable resource identifier. |
| `platform_en` / `platform_zh` | Platform, company, project, or provider name. |
| `product_or_resource` | Product, data resource, repository, API, SDK, CLI, MCP, or Skill name. |
| `domain_en` / `domain_zh` | Industry or domain. |
| `country_region` | Country or region when known. |
| `resource_formats` | Access formats, such as `CLI`, `MCP`, `Skill`, `SDK/API`, `Plugin`, or `Data export`. |
| `source_format` | Evidence/source format, such as `github_repo`, `official_web`, `api_docs`, or `dataset_portal`. |
| `official_cli` / `official_skill` / `official_mcp` / `official_sdk_api` | Official access-path evidence or status. |
| `source_url` | Primary official or evidence URL. |
| `official_status_en` / `official_status_zh` | Official-source status. |
| `verification_status` | Original review status. |
| `openness_level` | Interface or data openness notes. |
| `risk_level` | Rough access-surface risk label. |
| `description_en` / `description_zh` | Notes or description. |
| `source_dataset` | Original import batch or source. |
| `checked_at` | Last checked date. |
| `sort_order` | User-facing display priority. |

## `tracked_entities`

| Field | Description |
|---|---|
| `entity_id` | Stable tracked entity identifier. |
| `entity_name_en` / `entity_name_zh` | Company, platform, public data source, or software name. |
| `entity_type` | Entity type, such as public data source, professional software, company, or software platform. |
| `domain_en` / `domain_zh` | Domain for tracking and candidate classification. |
| `official_homepage` / `primary_github` / `primary_docs` | Official sources used for tracking and double-checking. |
| `commercial_model` | Free, paid, mixed, open-source, subscription, institution-license, or other access model. |
| `tracking_status` | Tracking lifecycle status. |
| `index_status` | Whether the entity already has indexed resources. |
| `watch_count` / `candidate_count` | Tracking-source and candidate counts. |
| `last_discovered_at` / `last_reviewed_at` / `last_promoted_at` | Lifecycle timestamps. |
| `watch_sources_json` | JSON array of official sources to poll. |

Regenerate readable exports after SQLite updates:

```bash
python3 scripts/export_formats.py
```
