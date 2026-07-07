# Candidate Tracking System

This project can run scheduled discovery and pre-review for new access-resource candidates.

The tracking system is intentionally conservative:

- It writes candidates into `data/09-candidates/`.
- It does not modify the primary CSV database.
- Agent or human review must confirm evidence before promotion.
- Medical and biological tracking is limited to public, publicly obtainable, or commercially licensed data resources and public/professional software. It excludes private patient data, PHI, PII, hospital-internal systems, and institution-internal datasets.

## Pipeline

```text
data/05-tracked-entities.csv
        |
        v
data/06-tracking-watchlist.csv
        |
        v
scripts/discover_candidates.py
        |
        v
data/09-candidates/discovered-YYYY-MM-DD.jsonl
        |
        v
scripts/review_candidates.py
        |
        v
data/09-candidates/reviewed-YYYY-MM-DD.jsonl
data/09-candidates/review-queue.md
        |
        v
scripts/sync_tracking_status.py
        |
        v
data/05-tracked-entities.csv
```

## Discovery

Run discovery locally:

```bash
python3 scripts/discover_candidates.py
```

The script follows the persistent watchlist in `data/06-tracking-watchlist.csv`. Set `GITHUB_TOKEN` to increase GitHub rate limits.

## Tracked Entities

`data/05-tracked-entities.csv` is the company/platform/resource base table. It stores stable entity information and tracking status. The watchlist links back to it through `entity_id`.

Use this table to answer:

- Which companies, datasets, platforms, or software projects are tracked?
- Which tracked entities are already indexed?
- Which ones have candidate updates?
- Which ones need review or are paused?

Important fields:

| Field | Meaning |
|---|---|
| `entity_id` | Stable entity key used by watchlist and candidate records. |
| `entity_name_en` / `entity_name_zh` | Company, platform, dataset, or software name. |
| `entity_type` | `Public data source`, `Professional software`, `Software platform`, etc. |
| `official_homepage` | Primary official home page. |
| `primary_github` | Main official GitHub org/repo when available. |
| `primary_docs` | Main official documentation or developer page. |
| `commercial_model` | Free, open source, subscription, commercial, institution license, etc. |
| `tracking_status` | `active`, `paused`, `needs_review`, or another local status. |
| `index_status` | `indexed`, `not_indexed`, `partial`, or local review status. |
| `watch_count` | Number of watchlist rows linked to the entity. |
| `candidate_count` | Latest discovered candidate count linked to the entity. |
| `last_discovered_at` / `last_reviewed_at` / `last_promoted_at` | Lifecycle timestamps. |

## Watchlist

The watchlist is the system's "待追踪 list". Each row describes one official source to follow for a tracked entity.

| Field | Meaning |
|---|---|
| `watch_id` | Stable tracking ID. |
| `entity_id` | Links this source to `data/05-tracked-entities.csv`. |
| `domain_zh` / `domain_en` | Domain for candidate classification. |
| `target_name` | Vendor, platform, database, software, or official project name. |
| `source_type` | `github_org`, `github_user`, `github_repo`, `rss`, `atom`, or `web_page`. |
| `source_url` | Official source to poll. |
| `official_homepage` | Official home page for double-checking. |
| `keywords` | Semicolon-delimited filters such as `cli;mcp;sdk;api;skill;SKILL.md`. |
| `exclude_terms` | Boundary filters for private, patient-level, or internal data. |
| `notes` | Why this source is tracked. |
| `checked_at` | Last manual review date. |

Only matching items become candidates. Non-matching updates stay out of the review queue.

## Review

Run pre-review:

```bash
python3 scripts/review_candidates.py
```

The review step assigns a rule-based recommendation:

| Status | Meaning |
|---|---|
| `Candidate - likely official` | Strong candidate, but still needs evidence confirmation. |
| `Candidate - needs evidence` | Relevant machine-access signal found; official status is not yet clear. |
| `Low priority` | Weak or noisy candidate. |
| `Duplicate` | Already appears in source data. |
| `Rejected - boundary` | Appears to cross private, patient-level, or sensitive-data boundaries. |

## Promotion

Before a candidate enters the primary database, confirm at least one evidence source:

- Official GitHub organization.
- Official vendor or institution domain.
- Official documentation.
- Product-team README or release note.

Then add it to the relevant source table:

- `data/03-vendor-openness-matrix.csv` for industry-level coverage.
- `data/02-platforms.csv` for reverse lookup by platform/software name.
- `data/04-agent-skill-ecosystem.csv` for Agent Skill ecosystem entries.

After editing source CSV files, regenerate derived files:

```bash
python3 scripts/build_access_resources.py
python3 scripts/export_formats.py
```

Then sync entity tracking status:

```bash
python3 scripts/sync_tracking_status.py
```

## Double Check

Before promotion, the reviewer should check:

- The candidate came from an official website, RSS/Atom feed, GitHub org, or official repository.
- The source actually exposes CLI, MCP, SDK, API, Agent Skill, webhook, data export, or a machine-readable interface.
- The data/resource is public, publicly obtainable, or commercially licensed; it does not require private patient data, PHI, PII, or internal institutional access.
- The official evidence URL is stable enough to cite in the CSV.

## Scheduled Runs

GitHub Actions workflow:

```text
.github/workflows/candidate-tracking.yml
```

It runs weekly and can also be started manually from the Actions tab.
