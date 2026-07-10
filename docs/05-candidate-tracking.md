# Candidate Tracking System

The tracking system follows public, official, or commercially obtainable sources only. It excludes private patient data, PHI, PII, hospital-internal systems, institution-internal datasets, and proprietary non-public data.

## Pipeline

```text
data/01-index.sqlite
  tracked_entities.watch_sources_json
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
data/01-index.sqlite
data/02-tracked-entities.*.csv
```

## Tracked Entities

The "待追踪 list" lives in the `tracked_entities` table. Each entity can include multiple sources in `watch_sources_json`.

Typical watch-source fields:

| Field | Meaning |
|---|---|
| `watch_id` | Stable tracking source ID. |
| `entity_id` | Linked tracked entity. |
| `target_name` | Vendor, platform, database, software, or official project name. |
| `source_type` | `github_org`, `github_user`, `github_repo`, `rss`, `atom`, or `web_page`. |
| `source_url` | Official source to poll. |
| `official_homepage` | Official home page for double-checking. |
| `keywords` | Semicolon-delimited filters such as `cli;mcp;sdk;api;skill;SKILL.md`. |
| `exclude_terms` | Boundary filters for private, patient-level, or internal data. |

Only matching items become candidates. Non-matching updates stay out of the review queue.

## Source Types

The current discovery script supports:

| Source type | What it checks |
|---|---|
| `github_org` | Recent repositories under an official GitHub organization. |
| `github_user` | Recent repositories under an official GitHub user account. |
| `github_repo` | One official repository, including description, topics, homepage, and update metadata. |
| `rss` / `atom` | Feed entries from official release, changelog, blog, or docs feeds. |
| `web_page` | One official public page, such as API docs, release pages, or developer documentation. |

`scripts/sync_entities_from_sources.py` auto-generates watch sources from each tracked entity's `primary_github`, `primary_docs`, and `official_homepage`. Entities without a usable public URL remain in the table with `needs_source` status so they can be completed later.

GitHub repositories also get generated Atom feed sources for releases and commits when possible. The preferred scan order is GitHub API/CLI and feeds first, then public web pages.

## Incremental State

Discovery is incremental. Runtime state is stored in the SQLite `tracking_state` table:

| Field | Meaning |
|---|---|
| `watch_id` | Linked watch source. |
| `last_checked_at` / `last_success_at` | Latest scan and latest successful scan. |
| `last_seen_signature` | Latest update marker, such as GitHub `pushed_at` or feed updated date. |
| `next_check_after` | Next due time for this watch source. |
| `failure_count` | Consecutive failures. |
| `fallback_method` / `fallback_count` | Fallback used for difficult sources, such as `crawl4ai`. |
| `notes` | Operational notes, including degraded/fallback handling. |

Default scan frequencies are shorter for GitHub and feeds, and longer for ordinary web pages. Use `--force` only for audits or backfills.

Useful options:

```bash
python3 scripts/discover_candidates.py --limit-per-source 20
python3 scripts/discover_candidates.py --force --limit-per-source 20
python3 scripts/discover_candidates.py --max-sources 20 --limit-per-source 5
```

For non-GitHub web pages, the scanner first uses a fast HTTP request. If that fails and `crawl4ai` is available, it falls back to Crawl4AI and records the fallback in `tracking_state`, then lowers the scan frequency to avoid repeated slow crawls.

## Review

Run the local pipeline:

```bash
python3 scripts/discover_candidates.py
python3 scripts/review_candidates.py
python3 scripts/sync_tracking_status.py
```

The review step assigns a rule-based recommendation:

| Status | Meaning |
|---|---|
| `Candidate - likely official` | Strong candidate, but still needs evidence confirmation. |
| `Candidate - needs evidence` | Relevant machine-access signal found; official status is not yet clear. |
| `Low priority` | Weak or noisy candidate. |
| `Duplicate` | Already appears in `data_sources`. |
| `Rejected - boundary` | Appears to cross private, patient-level, or sensitive-data boundaries. |

## Promotion

Before a candidate enters `data_sources`, confirm:

- The candidate came from an official website, RSS/Atom feed, GitHub org/repo, docs page, or product-team source.
- The source exposes CLI, MCP, SDK, API, Agent Skill, webhook, data export, or another machine-readable interface.
- The resource is public, publicly obtainable, or commercially licensed.
- The evidence URL is stable enough to cite.

After updating SQLite, regenerate readable exports and README statistics:

```bash
python3 scripts/export_formats.py
```

## Scheduled Runs

GitHub Actions workflow:

```text
.github/workflows/candidate-tracking.yml
```

It runs weekly and can also be started manually from the Actions tab.
