<p align="center">
  <img src="assets/banner.svg" alt="Agent Access Entropy Index banner" width="100%">
</p>

# Agent Access Entropy Index

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-draft--index-blue)
![Data](https://img.shields.io/badge/data-CSV%20%2B%20Markdown-informational)

English | [中文](README.zh-CN.md)

**Agent Access Entropy Index** is a community-maintained index of official-source CLI, Agent Skill, MCP, SDK, and API access paths for software platforms, data providers, financial terminals, social platforms, crypto exchanges, cloud services, and developer tools.

It asks a simple question:

> How much reliable, official-source, machine-readable access does a platform expose to AI agents and developers?

## Quick Start

To check whether a platform has official CLI, MCP, Agent Skill, SDK, or API access, query the primary CSV:

```bash
python3 - <<'PY'
import csv

keyword = "GitHub"
with open("data/01-access-resources.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        text = " ".join(row.values())
        if keyword.lower() in text.lower():
            print(row["platform_en"], row["access_resource_types"], row["source_url"])
PY
```

Use SQLite for aggregation:

```bash
sqlite3 data/01-access-resources.sqlite \
  "SELECT domain_en, access_resource_types, COUNT(*) FROM access_resources GROUP BY domain_en, access_resource_types ORDER BY COUNT(*) DESC LIMIT 20;"
```

Agents and automation pipelines can read JSONL directly:

```bash
jq 'select(.domain_en == "Crypto trading") | {platform_en, access_resource_types, source_url}' data/01-access-resources.jsonl
```

To track new official sources over time, maintain `data/05-tracked-entities.csv` and `data/06-tracking-watchlist.csv`, then run:

```bash
python3 scripts/discover_candidates.py
python3 scripts/review_candidates.py
python3 scripts/sync_tracking_status.py
```

Candidate outputs are written to `data/09-candidates/`. They are pre-review signals, not verified database entries.

<!-- resource-stats:start -->
## Dataset Snapshot

Current coverage:

| Metric | Count |
|---|---:|
| Access resources | 202 |
| Platforms / software | 70 |
| Industries / domains | 45 |

Largest domains:

- Crypto trading: 39
- Office and collaboration: 17
- Financial data and terminals: 17
- Social media: 14
- Cloud, data, and AI: 14

Dataset version: `0.1.0`.
<!-- resource-stats:end -->

## Concept

**Agent access entropy** describes the diversity and reliability of official-source access paths available to agents and developers.

A platform has higher access entropy when it exposes multiple well-documented, machine-readable, automatable paths such as CLI, MCP, Agent Skills, SDKs, APIs, webhooks, or data exports. It has lower access entropy when access is closed, undocumented, UI-only, or dependent on unofficial wrappers.

The index can be used at both platform and industry level: a platform score describes one product's access entropy, while an industry score aggregates the access entropy of multiple important platforms in that field.

## Status And Disclaimer

This project is an independent research index. It is not affiliated with, endorsed by, sponsored by, or officially approved by any listed vendor, platform, exchange, data provider, product, or GitHub organization.

The word "official" means that a source appears to be published by the vendor's official GitHub organization, official domain, documentation, or clearly identified product team.

This repository is an index, not a security audit. See [Disclaimer](docs/11-disclaimer.md).

## What's Included

- Official CLIs.
- Official Agent Skills and `SKILL.md` repositories.
- Official MCP servers and MCP plugins.
- Official SDKs and APIs.
- Community projects where no official source has been found.
- Verification status and evidence links.
- Risk notes for finance, crypto trading, payments, and sensitive data workflows.

## Data

| File | Description |
|---|---|
| [`data/01-access-resources.csv`](data/01-access-resources.csv) | Primary unified table for looking up official-source access resources by platform. |
| [`data/01-access-resources.jsonl`](data/01-access-resources.jsonl) | Agent-friendly JSONL export, one resource per line. |
| [`data/01-access-resources.sqlite`](data/01-access-resources.sqlite) | Local SQLite database for SQL queries and aggregation. |
| [`data/07-schema.json`](data/07-schema.json) | JSON Schema for the unified access resource record. |
| [`data/08-manifest.json`](data/08-manifest.json) | Dataset version, row count, generated files, and checksums. |
| [`data/02-platforms.csv`](data/02-platforms.csv) | Reverse lookup by platform/software name across social, office, finance, crypto, developer, cloud, data, and AI platforms. |
| [`data/03-vendor-openness-matrix.csv`](data/03-vendor-openness-matrix.csv) | Industry-level openness matrix for official CLI, Skill, MCP, SDK, and API availability. |
| [`data/04-agent-skill-ecosystem.csv`](data/04-agent-skill-ecosystem.csv) | Earlier ecosystem database focused on Agent Skill providers. |
| [`data/05-tracked-entities.csv`](data/05-tracked-entities.csv) | Base table for tracked companies, platforms, public data resources, and professional software. |
| [`data/06-tracking-watchlist.csv`](data/06-tracking-watchlist.csv) | Official source watchlist for scheduled tracking by entity. |
| [`data/09-candidates/review-queue.md`](data/09-candidates/review-queue.md) | Transparent pre-review queue generated from tracked sources. |

## Documentation

| Document | Description |
|---|---|
| [Reverse Platform Audit](docs/06-reverse-platform-audit.md) | Human-readable audit by platform/software name. |
| [Vendor Openness Matrix](docs/07-vendor-openness-matrix.md) | Industry matrix and observations. |
| [Official Skill/MCP Audit](docs/08-official-skill-mcp-audit.md) | Focused audit of confirmed official Skill/MCP sources. |
| [Agent Skill Ecosystem Database](docs/09-agent-skill-ecosystem-database.md) | Agent Skill ecosystem notes. |
| [Data Dictionary](docs/03-data-dictionary.md) | CSV field definitions. |
| [Query Guide](docs/04-query-guide.md) | How to query CSV, JSONL, SQLite, and MCP tools. |
| [Candidate Tracking](docs/05-candidate-tracking.md) | How to maintain tracked entities, official source watchlists, candidate queues, and index status. |
| [Methodology](docs/01-methodology.md) | Access path definitions and scoring draft. |
| [Verification Policy](docs/02-verification-policy.md) | Rules for marking a source as official, partial, community, or unconfirmed. |
| [Contributing](docs/10-contributing.md) | Contribution guidelines. |
| [Disclaimer](docs/11-disclaimer.md) | Legal, security, finance, and trademark disclaimers. |

## Highlighted Confirmed Sources

| Category | Platform | Official Source |
|---|---|---|
| Developer platform | GitHub | [`cli/cli`](https://github.com/cli/cli), [`github/github-mcp-server`](https://github.com/github/github-mcp-server) |
| Office / collaboration | Lark / Feishu | [`larksuite/cli`](https://github.com/larksuite/cli) |
| Office / collaboration | DingTalk | [`DingTalk-Real-AI/dingtalk-workspace-cli`](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli) |
| Office / documents | WPS / Kdocs | [`WPS-SmartDocs/WPS-AirPage-Skill`](https://github.com/WPS-SmartDocs/WPS-AirPage-Skill) |
| Knowledge base | Yuque | [`yuque/yuque-ecosystem`](https://github.com/yuque/yuque-ecosystem) |
| Finance data | Wind | [`Wind-Information-Co-Ltd/wind-skills`](https://github.com/Wind-Information-Co-Ltd/wind-skills) |
| Finance data | iFinD | [iFinD MCP platform](https://mcp.51ifind.com/) |
| Crypto | Binance | [`binance/binance-skills-hub`](https://github.com/binance/binance-skills-hub) |
| Crypto | Coinbase | [`coinbase/agentic-wallet-skills`](https://github.com/coinbase/agentic-wallet-skills), [`coinbase/agentkit`](https://github.com/coinbase/agentkit), [`coinbase/payments-mcp`](https://github.com/coinbase/payments-mcp) |
| Crypto | OKX | [`okx/agent-skills`](https://github.com/okx/agent-skills), [`okx/agent-trade-kit`](https://github.com/okx/agent-trade-kit) |
| Crypto | Kraken | [`krakenfx/kraken-cli`](https://github.com/krakenfx/kraken-cli) |
| Crypto market data | CoinMarketCap | [`coinmarketcap-official/skills-for-ai-agents-by-CoinMarketCap`](https://github.com/coinmarketcap-official/skills-for-ai-agents-by-CoinMarketCap) |

## Scoring Draft

A simple industry-level Agent Access Entropy score can be estimated from the existing CSV fields:

```text
Platform Entropy = Access × Velocity × Openness × Reliability
Industry Entropy = Σ Platform Entropy
Agent Access Entropy Index = 100 × Industry Entropy / MaxPossibleEntropy
```

Suggested interpretation:

| Score | Meaning |
|---:|---|
| 0-20 | Closed or low machine access |
| 20-40 | Limited flow |
| 40-60 | Moderate flow |
| 60-80 | High flow |
| 80-100 | Highly open, fast machine-readable flow |

Risk should be tracked separately from openness. Crypto trading, payments, account changes, production writes, and on-chain signing are high-risk even when official access is strong.

## AI-Friendly Access

The repository ships multiple local-first access formats:

```text
data/
  01-access-resources.csv
  01-access-resources.jsonl
  01-access-resources.sqlite
  07-schema.json
  08-manifest.json
```

`data/01-access-resources.csv` is the primary dataset. The JSONL, SQLite, schema, and manifest files are derived artifacts generated from the CSV.

Regenerate derived files after editing the CSV:

```bash
python3 scripts/export_formats.py
```

This also refreshes the generated resource-count block in both README files.

For agent-native access, run the stdio MCP server:

```bash
python3 mcp/server.py
```

MCP tools include `search_platform`, `list_access_resources`, `filter_by_resource_type`, `list_official_mcp`, and `industry_summary`.

See [Query Guide](docs/04-query-guide.md).

## Candidate Tracking

Scheduled tracking follows `data/05-tracked-entities.csv` and `data/06-tracking-watchlist.csv`.
Discovery writes transparent candidate artifacts under `data/09-candidates/`; these are pre-review signals, not verified database entries.

Run locally:

```bash
python3 scripts/discover_candidates.py
python3 scripts/review_candidates.py
python3 scripts/sync_tracking_status.py
```

See [Candidate Tracking](docs/05-candidate-tracking.md).

## Versioning

Dataset/package version is stored in [`VERSION`](VERSION). Release notes are tracked in [`CHANGELOG.md`](CHANGELOG.md).

The current data manifest is [`data/08-manifest.json`](data/08-manifest.json). It records the version, row count, generated date, and SHA-256 checksums for the primary and derived data files.

## Safety Notes

Listed projects may execute commands, access private files, call external services, read or write business data, trigger payments, place trades, transfer crypto, or sign blockchain transactions.

Before using any listed CLI, Skill, MCP server, plugin, SDK, or script:

- Review source code and permissions.
- Prefer read-only credentials.
- Use sandbox or paper trading environments where possible.
- Require human confirmation for irreversible actions.
- Keep API keys, wallet keys, and secrets out of prompts and logs.

## Contributing

Corrections and additions are welcome. Please include an official source URL and evidence type when proposing a new entry.

See [Contributing](docs/10-contributing.md) and [Verification Policy](docs/02-verification-policy.md).

## Security

See [Security Policy](SECURITY.md). Please report malicious links, impersonation, or unsafe classifications through GitHub issues.

## License

MIT License. See [LICENSE](LICENSE).
