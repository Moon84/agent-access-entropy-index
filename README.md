<p align="center">
  <img src="assets/banner.svg" alt="Agent Access Entropy Index banner" width="100%">
</p>

# Agent Access Entropy Index

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-draft--index-blue)
![Data](https://img.shields.io/badge/data-SQLite%20%2B%20CSV-informational)

English | [Chinese](README.zh-CN.md)

Information entropy is the first principle of the AI era.

<!-- resource-stats:start -->
## Dataset Snapshot

| Access resources | Platforms / software | Industries / domains | Official source ratio | Access Index |
|---:|---:|---:|---:|---:|
| 318 | 246 | 58 | 168 / 318 (52.8%) | 61.4 / 100 |

### Industry Coverage

| Industry / domain | Resources | Distribution | Official sources | Official share |
|---|---:|---|---:|---:|
| Office and collaboration | 43 | `████████████▓▓▓▓▓▓▓▓▓▓▓▓` | 21 | 48.8% |
| Crypto trading | 39 | `████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ` | 14 | 35.9% |
| Social media | 23 | `███▓▓▓▓▓▓▓▓▓▓           ` | 6 | 26.1% |
| Financial data and terminals | 20 | `█▓▓▓▓▓▓▓▓▓▓             ` | 2 | 10.0% |
| Documents and knowledge bases | 18 | `█████▓▓▓▓▓              ` | 9 | 50.0% |
| Life sciences and biomedical research | 17 | `█████████               ` | 17 | 100.0% |
| Cloud and cloud native | 14 | `█████▓▓▓                ` | 9 | 64.3% |
| Cloud, data, and AI | 14 | `███████▓                ` | 13 | 92.9% |
| Financial data | 12 | `███▓▓▓▓                 ` | 5 | 41.7% |
| Data providers | 10 | `▓▓▓▓▓▓                  ` | 0 | 0.0% |
| Payments, commerce, CRM, and communications | 9 | `█▓▓▓▓                   ` | 1 | 11.1% |
| Data platforms and databases | 8 | `██▓▓                    ` | 5 | 62.5% |

Access Index = `100 * (0.7 * official_source_ratio + 0.3 * industry_entropy_score)`. The chart shows the top 12 industries by resource count; `█` means official sources, `▓` means unconfirmed or non-official sources, and blank space is unfilled length. The industry entropy score is 81.2% across all industries.

Primary data: `data/01-index.sqlite`. Version: `0.1.0`.
<!-- resource-stats:end -->

## Use The Data

Query the primary SQLite database:

```bash
sqlite3 data/01-index.sqlite \
  "SELECT platform_en, resource_formats, source_url FROM data_sources WHERE platform_en LIKE '%GitHub%' LIMIT 10;"
```

Open the readable CSV exports:

| File | Purpose |
|---|---|
| [`data/01-index.sqlite`](data/01-index.sqlite) | Primary database with three tables: `data_sources`, `tracked_entities`, and `schema_fields`. |
| [`data/01-data-sources.en.csv`](data/01-data-sources.en.csv) | English readable export of access resources. |
| [`data/01-data-sources.zh-CN.csv`](data/01-data-sources.zh-CN.csv) | Chinese readable export of access resources. |
| [`data/02-tracked-entities.en.csv`](data/02-tracked-entities.en.csv) | English readable export of tracked companies, platforms, software, and public data sources. |
| [`data/02-tracked-entities.zh-CN.csv`](data/02-tracked-entities.zh-CN.csv) | Chinese readable export of tracked companies, platforms, software, and public data sources. |
| [`data/03-schema.csv`](data/03-schema.csv) | Schema table export for the three SQLite tables. |
| [`data/04-manifest.json`](data/04-manifest.json) | Version, counts, generated files, and checksums. |

Refresh readable exports and README statistics after updating SQLite:

```bash
python3 scripts/export_formats.py
```

## What Is Included

- Official-source CLI, MCP, Agent Skill, SDK, API, plugin, and data-export access paths.
- Public or commercially obtainable data resources and public/professional software, including medical and biological domains.
- A tracked entity list connected to official websites, RSS/Atom feeds, GitHub orgs/repos, docs, and public pages.
- Pre-review candidate outputs under [`data/09-candidates/`](data/09-candidates/).

Private, patient-level, PHI/PII, institution-internal, and proprietary non-public datasets are outside the collection boundary.

## Tracking

Run the local tracking pipeline:

```bash
python3 scripts/discover_candidates.py
python3 scripts/review_candidates.py
python3 scripts/sync_tracking_status.py
```

The tracking system writes candidates first, then uses rule-based review and double-check evidence before anything is promoted into `data_sources`.

Current tracking source types include GitHub orgs/repos, official docs/homepages, RSS/Atom feeds, and public web pages. Entities without a usable public source are kept in the tracking table with `needs_source` status.

## Agent Access

Run the local stdio MCP server:

```bash
python3 mcp/server.py
```

MCP tools include `search_platform`, `list_access_resources`, `filter_by_resource_type`, `list_official_mcp`, and `industry_summary`.

## Documentation

| Document | Description |
|---|---|
| [Data Dictionary](docs/03-data-dictionary.md) | Three-table schema and readable CSV exports. |
| [Query Guide](docs/04-query-guide.md) | SQLite and MCP query examples. |
| [Candidate Tracking](docs/05-candidate-tracking.md) | Tracking list, candidate review, and promotion workflow. |
| [Methodology](docs/01-methodology.md) | Access path definitions and scoring draft. |
| [Verification Policy](docs/02-verification-policy.md) | Rules for official, partial, community, or unconfirmed sources. |
| [Contributing](docs/10-contributing.md) | Contribution guidelines. |
| [Disclaimer](docs/11-disclaimer.md) | Legal, security, finance, and trademark disclaimers. |

## Safety

Listed projects may execute commands, access private files, call external services, read or write business data, trigger payments, place trades, transfer crypto, or sign blockchain transactions. Review source code and permissions, use read-only credentials where possible, and require human confirmation for irreversible actions.

## License

MIT License. See [LICENSE](LICENSE).
