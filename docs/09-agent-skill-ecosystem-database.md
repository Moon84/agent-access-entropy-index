# Agent Skill Ecosystem Dataset

This document explains the purpose and maintenance rules for the Agent Skill ecosystem dataset. It intentionally does **not** list individual vendors, projects, or rankings.

For the actual records, use:

- [`../data/01-index.sqlite`](../data/01-index.sqlite), table `data_sources`
- [`../data/01-data-sources.en.csv`](../data/01-data-sources.en.csv)
- [`../data/01-data-sources.zh-CN.csv`](../data/01-data-sources.zh-CN.csv)
- [`06-reverse-platform-audit.md`](06-reverse-platform-audit.md)
- [`07-vendor-openness-matrix.md`](07-vendor-openness-matrix.md)
- [`08-official-skill-mcp-audit.md`](08-official-skill-mcp-audit.md)

## Purpose

The Agent Skill ecosystem dataset tracks public Agent Skill, CLI Skill, MCP, plugin, SDK, and API access paths that are relevant to AI agents and developer automation.

It is used as one input for the broader **Agent Access Entropy Index**.

## Scope

The dataset focuses on:

- Official Agent Skills and `SKILL.md` repositories.
- Official CLIs with agent-oriented usage.
- Official MCP servers and MCP plugins.
- Official SDKs and APIs that can support agent workflows.
- Community projects only when no official source is found or when they are important ecosystem references.

## Status Labels

| Status | Meaning |
|---|---|
| Official | Published by an official company, product, or vendor GitHub organization/team. |
| Quasi-official | Published by a founder, core maintainer, or closely affiliated team, but not under the primary official organization. |
| Community-leading | Not official, but influential by usage, coverage, stars, or ecosystem role. |
| Community | Third-party project with limited official evidence. |
| Not found | No official Skill, CLI, or MCP source has been found yet. |
| Pending verification | Candidate source exists but official status needs more evidence. |

## Skill Type Labels

| Type | Meaning |
|---|---|
| Agent Skill | A `SKILL.md` file or skill directory intended for agent runtimes. |
| CLI + Skill | A CLI bundled with, or documented for, agent skill usage. |
| MCP + Skill | MCP server/plugin plus Skill instructions or related agent workflow. |
| Plugin | Packaged extension for an agent environment. |
| SDK/API | Official programmatic interface that can support agent workflows. |
| Community wrapper | Third-party wrapper around an official product or API. |

## Fields

The `data_sources` table uses these fields:

| Field | Description |
|---|---|
| `resource_id` | Stable row identifier. |
| `platform_en` / `platform_zh` | Company, vendor, project, or maintainer. |
| `product_or_resource` | Product, platform, repository, or skill name. |
| `country_region` | Country or region when known. |
| `domain_en` / `domain_zh` | Industry/category. |
| `official_status_en` / `official_status_zh` | Official status label. |
| `resource_formats` | Access path type. |
| `source_url` | GitHub or official source URL. |
| `description_en` / `description_zh` | Additional notes. |
| `checked_at` | Last checked date. |

## Verification Rules

Use the repository-wide [Verification Policy](02-verification-policy.md).

In short, mark a source as official only when at least one condition is met:

- It is hosted under the vendor's official GitHub organization.
- It is linked from the vendor's official website or documentation.
- The README clearly identifies the repository as maintained by the official product team.

If evidence is incomplete, use a weaker status such as community, quasi-official, or pending verification.

## Maintenance Rules

- Keep this document as methodology and data documentation only.
- Do not list individual companies, products, or rankings here.
- Put records in the SQLite `data_sources` table and regenerate readable CSV exports.
- Put narrative audits and industry observations in the dedicated audit documents.
- Prefer source URLs over copied descriptions.
- Avoid promotional wording.
- Separate openness from safety: a highly open interface can still be high risk.

## Related Documents

| Document | Purpose |
|---|---|
| [Data Dictionary](03-data-dictionary.md) | Field definitions for the SQLite tables and CSV exports. |
| [Methodology](01-methodology.md) | Agent Access Entropy scoring approach. |
| [Verification Policy](02-verification-policy.md) | Official-source classification rules. |
| [Disclaimer](11-disclaimer.md) | Legal, security, finance, and trademark disclaimers. |
