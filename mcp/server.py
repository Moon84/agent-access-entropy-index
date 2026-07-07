#!/usr/bin/env python3
"""Minimal stdio MCP server for Agent Access Entropy Index.

This implementation intentionally uses only the Python standard library so the
repository remains easy to run locally.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from index_store import data_sources


ROOT = Path(__file__).resolve().parents[1]


def load_rows() -> list[dict[str, str]]:
    return [{key: str(value or "") for key, value in row.items()} for row in data_sources()]


ROWS = load_rows()


def text_response(payload: Any) -> dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(payload, ensure_ascii=False, indent=2),
            }
        ]
    }


def match_query(row: dict[str, str], query: str) -> bool:
    haystack = " ".join(
        [
            row.get("platform_en", ""),
            row.get("platform_zh", ""),
            row.get("product_or_resource", ""),
            row.get("domain_en", ""),
            row.get("domain_zh", ""),
            row.get("description_zh", ""),
            row.get("source_url", ""),
        ]
    ).lower()
    return query.lower() in haystack


def compact(row: dict[str, str]) -> dict[str, str]:
    keys = [
        "resource_id",
        "platform_en",
        "platform_zh",
        "product_or_resource",
        "domain_en",
        "domain_zh",
        "resource_formats",
        "source_url",
        "official_status_en",
        "official_status_zh",
        "risk_level",
        "checked_at",
    ]
    return {key: row.get(key, "") for key in keys}


def search_platform(query: str, limit: int = 10) -> list[dict[str, str]]:
    return [compact(row) for row in ROWS if match_query(row, query)][:limit]


def list_access_resources(platform: str, limit: int = 20) -> list[dict[str, str]]:
    return [compact(row) for row in ROWS if match_query(row, platform)][:limit]


def filter_by_resource_type(resource_type: str, limit: int = 50) -> list[dict[str, str]]:
    needle = resource_type.lower()
    return [
        compact(row)
        for row in ROWS
        if needle in row.get("resource_formats", "").lower()
    ][:limit]


def list_official_mcp(limit: int = 50) -> list[dict[str, str]]:
    return [
        compact(row)
        for row in ROWS
        if "mcp" in row.get("resource_formats", "").lower()
        and "未" not in row.get("official_mcp", "")
        and "unconfirmed" not in row.get("official_status_en", "").lower()
    ][:limit]


def industry_summary(domain: str | None = None) -> dict[str, Any]:
    rows = ROWS
    if domain:
        needle = domain.lower()
        rows = [
            row
            for row in rows
            if needle in row.get("domain_en", "").lower()
            or needle in row.get("domain_zh", "").lower()
        ]
    return {
        "rows": len(rows),
        "domains_en": Counter(row.get("domain_en", "") for row in rows).most_common(),
        "resource_types": Counter(
            item
            for row in rows
            for item in row.get("resource_formats", "").split(";")
            if item
        ).most_common(),
        "risk_levels": Counter(row.get("risk_level", "") for row in rows).most_common(),
    }


TOOLS = {
    "search_platform": {
        "description": "Search platforms/resources by keyword.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    },
    "list_access_resources": {
        "description": "List access resources for a platform.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "platform": {"type": "string"},
                "limit": {"type": "integer", "default": 20},
            },
            "required": ["platform"],
        },
    },
    "filter_by_resource_type": {
        "description": "Filter resources by type, such as CLI, Skill, MCP, SDK/API, or Plugin.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "resource_type": {"type": "string"},
                "limit": {"type": "integer", "default": 50},
            },
            "required": ["resource_type"],
        },
    },
    "list_official_mcp": {
        "description": "List resources with confirmed or likely official MCP access.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 50},
            },
        },
    },
    "industry_summary": {
        "description": "Summarize resource counts by domain, resource type, and risk.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string"},
            },
        },
    },
}


def handle_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "search_platform":
        return text_response(search_platform(args["query"], int(args.get("limit", 10))))
    if name == "list_access_resources":
        return text_response(list_access_resources(args["platform"], int(args.get("limit", 20))))
    if name == "filter_by_resource_type":
        return text_response(filter_by_resource_type(args["resource_type"], int(args.get("limit", 50))))
    if name == "list_official_mcp":
        return text_response(list_official_mcp(int(args.get("limit", 50))))
    if name == "industry_summary":
        return text_response(industry_summary(args.get("domain")))
    raise ValueError(f"unknown tool: {name}")


def send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    request_id = request.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "agent-access-entropy-index",
                    "version": "0.1.0",
                },
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {"name": name, **spec}
                    for name, spec in TOOLS.items()
                ]
            },
        }
    if method == "tools/call":
        params = request.get("params", {})
        result = handle_tool(params.get("name", ""), params.get("arguments", {}) or {})
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"method not found: {method}"},
    }


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            response = handle(json.loads(line))
        except Exception as exc:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32000, "message": str(exc)},
            }
        if response is not None:
            send(response)


if __name__ == "__main__":
    main()
