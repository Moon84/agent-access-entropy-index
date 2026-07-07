# Agent Skill Ecosystem Dataset

This document explains the purpose and maintenance rules for the Agent Skill ecosystem dataset. It intentionally does **not** list individual vendors, projects, or rankings.

For the actual records, use:

- [`../data/04-agent-skill-ecosystem.csv`](../data/04-agent-skill-ecosystem.csv)
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

The CSV uses these fields:

| Field | Description |
|---|---|
| `id` | Stable row identifier. |
| `company` | Company, vendor, project, or maintainer. |
| `product` | Product, platform, repository, or skill name. |
| `country_region` | Country or region when known. |
| `industry` | Industry/category. |
| `status` | Official status label. |
| `skill_type` | Access path type. |
| `github_url` | GitHub or official source URL. |
| `stars` | GitHub stars at time of collection, when available. |
| `skill_count` | Number of skills if the source is a skill collection. |
| `cli_relevance` | High / medium / low relevance to CLI usage. |
| `china_relevance` | High / medium / low relevance to China or Chinese-language platform ecosystems. |
| `leading_reason` | Short reason for inclusion. |
| `notes` | Additional notes. |
| `checked_at` | Last checked date. |

## Verification Rules

Use the repository-wide [Verification Policy](VERIFICATION_POLICY.md).

In short, mark a source as official only when at least one condition is met:

- It is hosted under the vendor's official GitHub organization.
- It is linked from the vendor's official website or documentation.
- The README clearly identifies the repository as maintained by the official product team.

If evidence is incomplete, use a weaker status such as community, quasi-official, or pending verification.

## Maintenance Rules

- Keep this document as methodology and data documentation only.
- Do not list individual companies, products, or rankings here.
- Put records in CSV files under [`../data`](../data).
- Put narrative audits and industry observations in the dedicated audit documents.
- Prefer source URLs over copied descriptions.
- Avoid promotional wording.
- Separate openness from safety: a highly open interface can still be high risk.

## Related Documents

| Document | Purpose |
|---|---|
| [Data Dictionary](DATA_DICTIONARY.md) | Field definitions for all CSV files. |
| [Methodology](METHODOLOGY.md) | Agent Access Entropy scoring approach. |
| [Verification Policy](VERIFICATION_POLICY.md) | Official-source classification rules. |
| [Disclaimer](DISCLAIMER.md) | Legal, security, finance, and trademark disclaimers. |
