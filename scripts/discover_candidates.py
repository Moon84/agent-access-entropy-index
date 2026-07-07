#!/usr/bin/env python3
"""Discover candidate access resources from tracked public sources.

The script writes JSONL into data/09-candidates/. It does not modify the primary
index; candidates must be reviewed before they are promoted into CSV data.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from index_store import known_urls as load_index_known_urls
from index_store import watchlist_rows


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CANDIDATES_DIR = DATA / "09-candidates"


def load_watchlist(path: Path) -> list[dict[str, str]]:
    if str(path) == "__sqlite__":
        return watchlist_rows()
    raise ValueError("watchlist CSV input has been retired; use the SQLite primary index")


def load_known_urls() -> set[str]:
    return load_index_known_urls()


def normalize_url(url: str) -> str:
    text = url.strip().rstrip("/")
    if text.startswith("http://"):
        text = "https://" + text[len("http://") :]
    return text


def github_request(path: str, token: str | None) -> dict[str, Any]:
    request = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "agent-access-entropy-index-discovery",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API error {exc.code}: {body}") from exc


def http_text(url: str, token: str | None = None) -> str:
    headers = {"User-Agent": "agent-access-entropy-index-discovery"}
    if "api.github.com" in url and token:
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/vnd.github+json"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in re.split(r"[;,]", value or "") if term.strip()]


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    lower = text.lower()
    hits: list[str] = []
    for keyword in keywords:
        needle = keyword.lower()
        if re.search(r"^[a-z0-9_.-]+$", needle):
            if re.search(rf"(?<![a-z0-9_.-]){re.escape(needle)}(?![a-z0-9_.-])", lower):
                hits.append(keyword)
        elif needle in lower:
            hits.append(keyword)
    return hits


def has_exclusion(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def repo_candidate(item: dict[str, Any], watch: dict[str, str], run_id: str, hits: list[str]) -> dict[str, Any]:
    owner = item.get("owner") or {}
    topics = item.get("topics") or []
    name = item.get("full_name", "")
    html_url = normalize_url(item.get("html_url", ""))
    text = " ".join(
        str(value or "")
        for value in [
            name,
            item.get("description", ""),
            " ".join(topics),
            item.get("homepage", ""),
        ]
    )
    return {
        "candidate_id": f"github:{name}",
        "discovered_at": run_id,
        "source_system": "github",
        "watch_id": watch["watch_id"],
        "entity_id": watch.get("entity_id", ""),
        "source_type": watch["source_type"],
        "tracking_source_url": watch["source_url"],
        "domain_zh": watch.get("domain_zh", ""),
        "domain_en": watch.get("domain_en", ""),
        "target_name": watch.get("target_name", ""),
        "platform_or_owner": owner.get("login", ""),
        "product_or_resource": name,
        "url": html_url,
        "homepage": item.get("homepage") or "",
        "description": item.get("description") or "",
        "stars": item.get("stargazers_count") or 0,
        "forks": item.get("forks_count") or 0,
        "language": item.get("language") or "",
        "topics": topics,
        "license": ((item.get("license") or {}).get("spdx_id") or ""),
        "created_at": item.get("created_at") or "",
        "updated_at": item.get("updated_at") or "",
        "pushed_at": item.get("pushed_at") or "",
        "archived": bool(item.get("archived")),
        "matched_keywords": hits,
        "resource_type_hints": infer_resource_type_hints(text),
        "raw_score": item.get("score") or 0,
    }


def infer_resource_type_hints(text: str) -> list[str]:
    lower = text.lower()
    hints: list[str] = []
    checks = [
        ("MCP", [r"\bmcp\b", r"model context protocol"]),
        ("Skill", [r"skill\.md", r"agent skill", r"\bskills?\b"]),
        ("CLI", [r"\bcli\b", r"command line", r"command-line"]),
        ("SDK/API", [r"\bsdk\b", r"\bapi\b", r"\brest\b", r"\bgraphql\b", r"\bopenapi\b"]),
        ("Data export", [r"\bdownload\b", r"\bdataset\b", r"data export"]),
    ]
    for label, patterns in checks:
        if any(re.search(pattern, lower) for pattern in patterns):
            hints.append(label)
    return hints


def github_api_path_from_url(url: str, source_type: str, limit: int) -> str:
    parsed = urllib.parse.urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 1:
        raise ValueError(f"invalid GitHub URL: {url}")
    owner = parts[0]
    if source_type == "github_org":
        return f"/orgs/{owner}/repos?sort=updated&direction=desc&per_page={limit}"
    if source_type == "github_user":
        return f"/users/{owner}/repos?sort=updated&direction=desc&per_page={limit}"
    if source_type == "github_repo" and len(parts) >= 2:
        return f"/repos/{owner}/{parts[1]}"
    raise ValueError(f"unsupported GitHub source: {source_type} {url}")


def discover_github_watch(watch: dict[str, str], limit: int, token: str | None, run_id: str) -> list[dict[str, Any]]:
    payload = github_request(github_api_path_from_url(watch["source_url"], watch["source_type"], limit), token)
    items = payload if isinstance(payload, list) else [payload]
    keywords = split_terms(watch.get("keywords", ""))
    exclusions = split_terms(watch.get("exclude_terms", ""))
    candidates: list[dict[str, Any]] = []
    for item in items:
        text = " ".join(
            str(value or "")
            for value in [
                item.get("full_name", ""),
                item.get("name", ""),
                item.get("description", ""),
                " ".join(item.get("topics") or []),
                item.get("homepage", ""),
            ]
        )
        hits = keyword_hits(text, keywords)
        if not hits or has_exclusion(text, exclusions):
            continue
        candidates.append(repo_candidate(item, watch, run_id, hits))
    return candidates


def discover_feed_watch(watch: dict[str, str], limit: int, run_id: str) -> list[dict[str, Any]]:
    text = http_text(watch["source_url"])
    root = ET.fromstring(text)
    keywords = split_terms(watch.get("keywords", ""))
    exclusions = split_terms(watch.get("exclude_terms", ""))
    candidates: list[dict[str, Any]] = []
    entries = root.findall(".//{http://www.w3.org/2005/Atom}entry") or root.findall(".//item")
    for entry in entries[:limit]:
        title = first_xml_text(entry, ["title"])
        summary = first_xml_text(entry, ["summary", "description", "content"])
        link = first_xml_link(entry)
        body = " ".join([title, summary, link])
        hits = keyword_hits(body, keywords)
        if not hits or has_exclusion(body, exclusions):
            continue
        candidates.append(generic_candidate(watch, run_id, "feed", title, link, summary, hits))
    return candidates


def first_xml_text(entry: ET.Element, names: list[str]) -> str:
    for name in names:
        found = entry.find(name) or entry.find(f"{{http://www.w3.org/2005/Atom}}{name}")
        if found is not None and found.text:
            return html.unescape(found.text.strip())
    return ""


def first_xml_link(entry: ET.Element) -> str:
    atom_link = entry.find("{http://www.w3.org/2005/Atom}link")
    if atom_link is not None and atom_link.get("href"):
        return atom_link.get("href", "")
    link = entry.find("link")
    return (link.text or "").strip() if link is not None else ""


def discover_web_page_watch(watch: dict[str, str], run_id: str) -> list[dict[str, Any]]:
    text = http_text(watch["source_url"])
    cleaned = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.I | re.S)
    plain = re.sub(r"<[^>]+>", " ", cleaned)
    plain = html.unescape(re.sub(r"\s+", " ", plain)).strip()
    hits = keyword_hits(plain, split_terms(watch.get("keywords", "")))
    if not hits or has_exclusion(plain, split_terms(watch.get("exclude_terms", ""))):
        return []
    title_match = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
    title = html.unescape(re.sub(r"\s+", " ", title_match.group(1)).strip()) if title_match else watch["target_name"]
    return [generic_candidate(watch, run_id, "web_page", title, watch["source_url"], plain[:500], hits)]


def generic_candidate(
    watch: dict[str, str],
    run_id: str,
    source_system: str,
    title: str,
    url: str,
    description: str,
    hits: list[str],
) -> dict[str, Any]:
    return {
        "candidate_id": f"{source_system}:{normalize_url(url)}",
        "discovered_at": run_id,
        "source_system": source_system,
        "watch_id": watch["watch_id"],
        "entity_id": watch.get("entity_id", ""),
        "source_type": watch["source_type"],
        "tracking_source_url": watch["source_url"],
        "domain_zh": watch.get("domain_zh", ""),
        "domain_en": watch.get("domain_en", ""),
        "target_name": watch.get("target_name", ""),
        "platform_or_owner": watch.get("target_name", ""),
        "product_or_resource": title,
        "url": normalize_url(url),
        "homepage": watch.get("official_homepage", ""),
        "description": description,
        "stars": 0,
        "forks": 0,
        "language": "",
        "topics": [],
        "license": "",
        "created_at": "",
        "updated_at": "",
        "pushed_at": "",
        "archived": False,
        "matched_keywords": hits,
        "resource_type_hints": infer_resource_type_hints(" ".join([title, description])),
        "raw_score": 0,
    }


def discover_watchlist(watchlist: list[dict[str, str]], limit: int, token: str | None, run_id: str) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for watch in watchlist:
        source_type = watch.get("source_type", "")
        try:
            if source_type in {"github_org", "github_user", "github_repo"}:
                candidates.extend(discover_github_watch(watch, limit, token, run_id))
            elif source_type in {"rss", "atom"}:
                candidates.extend(discover_feed_watch(watch, limit, run_id))
            elif source_type == "web_page":
                candidates.extend(discover_web_page_watch(watch, run_id))
            else:
                print(f"skipping unsupported source_type={source_type} watch_id={watch.get('watch_id')}", file=sys.stderr)
        except Exception as exc:
            print(f"warning: failed watch_id={watch.get('watch_id')}: {exc}", file=sys.stderr)
        time.sleep(1)
    return candidates


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover candidate access resources.")
    parser.add_argument("--watchlist", default="__sqlite__")
    parser.add_argument("--limit-per-source", type=int, default=20)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    watchlist = load_watchlist(Path(args.watchlist))
    known_urls = load_known_urls()
    run_id = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    token = os.environ.get("GITHUB_TOKEN")

    candidates = discover_watchlist(watchlist, args.limit_per_source, token, run_id)
    deduped: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        url = normalize_url(candidate["url"])
        if url in known_urls:
            continue
        deduped[candidate["candidate_id"]] = candidate

    output = Path(args.output) if args.output else CANDIDATES_DIR / f"discovered-{run_id[:10]}.jsonl"
    write_jsonl(output, list(deduped.values()))
    try:
        display_path = output.relative_to(ROOT)
    except ValueError:
        display_path = output
    print(f"wrote {len(deduped)} candidates to {display_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
