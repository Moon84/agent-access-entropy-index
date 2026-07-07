#!/usr/bin/env python3
"""Build the unified access resources table from source CSV files."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


FIELDS = [
    "resource_id",
    "platform_en",
    "platform_zh",
    "product_or_resource",
    "domain_en",
    "domain_zh",
    "country_region",
    "access_resource_types",
    "official_cli",
    "official_skill",
    "official_mcp",
    "official_sdk_api",
    "source_url",
    "official_status_en",
    "official_status_zh",
    "verification_status",
    "openness_level",
    "risk_level",
    "description_en",
    "description_zh",
    "source_dataset",
    "checked_at",
]


DOMAIN_EN = {
    "社交媒体": "Social media",
    "办公协作": "Office and collaboration",
    "金融数据": "Financial data",
    "数字货币交易": "Crypto trading",
    "开发者平台": "Developer platforms",
    "云数据AI": "Cloud, data, and AI",
    "企业协作与办公套件": "Office and collaboration",
    "企业协作与办公": "Office and collaboration",
    "办公套件": "Office suites",
    "文档与知识库": "Documents and knowledge bases",
    "金融数据与终端": "Financial data and terminals",
    "开发者平台与代码托管": "Developer platforms and code hosting",
    "公有云与云原生": "Cloud and cloud native",
    "数据平台与数据库": "Data platforms and databases",
    "数据供应商": "Data providers",
    "AI与模型平台": "AI and model platforms",
    "AI / 模型平台": "AI and model platforms",
    "AI / Agent": "AI and agent platforms",
    "Agent 工具平台": "Agent tool platforms",
    "Agent 框架": "Agent frameworks",
    "浏览器自动化": "Browser automation",
    "设计前端移动": "Design, frontend, and mobile",
    "前端框架": "Frontend frameworks",
    "跨平台开发": "Cross-platform development",
    "移动开发": "Mobile development",
    "React Native": "React Native",
    "设计工具": "Design tools",
    "Web 动效": "Web animation",
    "视频生成": "Video generation",
    "Headless CMS": "Headless CMS",
    "Web 质量": "Web quality",
    "测试": "Testing",
    "支付电商CRM通信": "Payments, commerce, CRM, and communications",
    "知识库与团队文档": "Knowledge bases and team documents",
    "社交内容与营销": "Social content and marketing",
    "Web 部署平台": "Web deployment platforms",
    "加密金融": "Crypto finance",
    "数据库": "Databases",
    "文档与办公": "Documents and office",
    "微信公众号内容发布": "WeChat Official Account publishing",
    "微信生态": "WeChat ecosystem",
    "知识管理": "Knowledge management",
    "科研与文献管理": "Research and reference management",
    "云边缘与安全": "Cloud, edge, and security",
    "知识库与协作": "Knowledge bases and collaboration",
    "企业软件与开发平台": "Enterprise software and developer platforms",
    "硬件半导体与 HPC": "Hardware, semiconductors, and HPC",
    "安全审计": "Security auditing",
    "可观测与错误监控": "Observability and error monitoring",
    "测试平台": "Testing platforms",
    "支付": "Payments",
    "数据库与分析": "Databases and analytics",
    "本地分析数据库": "Local analytics databases",
    "实时数据平台": "Realtime data platforms",
    "可观测": "Observability",
    "CMS": "CMS",
    "GraphQL 平台": "GraphQL platforms",
    "浏览器与搜索": "Browsers and search",
}


STATUS_EN = {
    "官方": "Official",
    "官方倾向": "Likely official",
    "准官方": "Quasi-official",
    "社区领先": "Community-leading",
    "社区": "Community",
    "未发现官方 Skill": "No official Skill found",
    "未发现官方": "No official source found",
    "未确认官方": "Official source unconfirmed",
    "未发现官方 Skill/MCP": "No official Skill/MCP found",
    "已确认": "Confirmed",
    "已确认 CLI": "Confirmed CLI",
    "已确认 Skill": "Confirmed Skill",
    "已确认 MCP": "Confirmed MCP",
    "已确认 Skill/MCP": "Confirmed Skill/MCP",
    "已确认 Skill/MCP 指引": "Confirmed Skill/MCP guidance",
    "已确认 CLI/MCP": "Confirmed CLI/MCP",
    "已确认 CLI/Skill": "Confirmed CLI/Skill",
    "已确认 SDK": "Confirmed SDK",
    "已确认 SDK/Skill": "Confirmed SDK/Skill",
    "已确认 API": "Confirmed API",
    "部分确认": "Partially confirmed",
    "待复核": "Pending verification",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def has_value(value: str) -> bool:
    text = (value or "").strip()
    if not text:
        return False
    negatives = ["未发现", "未确认", "待补", "无", "不明显"]
    return not any(token in text for token in negatives)


def split_platform(value: str) -> tuple[str, str]:
    text = (value or "").strip()
    if not text:
        return "", ""
    parts = [p.strip() for p in text.replace("／", "/").split("/")]
    zh = ""
    en = ""
    for part in parts:
        if any("\u4e00" <= ch <= "\u9fff" for ch in part):
            zh = zh or part
        else:
            en = en or part
    return en or text, zh or text


def resource_types(row: dict[str, str]) -> str:
    types: list[str] = []
    if has_value(row.get("official_cli", "")):
        types.append("CLI")
    if has_value(row.get("official_skill", "")) or "Skill" in row.get("skill_type", ""):
        types.append("Skill")
    if has_value(row.get("official_mcp", "")) or "MCP" in row.get("skill_type", ""):
        types.append("MCP")
    if has_value(row.get("api_sdk_open", "")) or "SDK" in row.get("skill_type", "") or "API" in row.get("skill_type", ""):
        types.append("SDK/API")
    if "Plugin" in row.get("skill_type", ""):
        types.append("Plugin")
    if not types and row.get("skill_type"):
        types.append(row["skill_type"])
    return ";".join(dict.fromkeys(types))


def official_status_zh(row: dict[str, str]) -> str:
    for key in ("status", "verification_status", "official_skill"):
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def infer_risk(row: dict[str, str]) -> str:
    text = " ".join(str(v) for v in row.values())
    critical_terms = ["转账", "签名", "wallet", "on-chain", "链上", "crypto", "交易", "trade", "trading", "order", "futures", "options"]
    high_terms = ["支付", "payment", "生产", "cloud", "账户", "account", "write", "写入", "deploy", "email", "messages"]
    if any(t.lower() in text.lower() for t in critical_terms):
        return "Critical"
    if any(t.lower() in text.lower() for t in high_terms):
        return "High"
    return "Medium"


def platform_key(row: dict[str, str]) -> tuple[str, str]:
    platform = row.get("platform") or row.get("company") or ""
    product = row.get("product") or row.get("product_or_platform") or ""
    url = row.get("official_source_url") or row.get("github_url") or ""
    return (platform.strip().lower(), product.strip().lower() or url.strip().lower())


def normalize_platform_row(row: dict[str, str], idx: int) -> dict[str, str]:
    platform_en, platform_zh = split_platform(row["platform"])
    domain_zh = row["domain"]
    return {
        "resource_id": f"aar-{idx:04d}",
        "platform_en": platform_en,
        "platform_zh": platform_zh,
        "product_or_resource": row["platform"],
        "domain_en": DOMAIN_EN.get(domain_zh, domain_zh),
        "domain_zh": domain_zh,
        "country_region": "",
        "access_resource_types": resource_types(row),
        "official_cli": row.get("official_cli", ""),
        "official_skill": row.get("official_skill", ""),
        "official_mcp": row.get("official_mcp", ""),
        "official_sdk_api": "",
        "source_url": row.get("official_source_url", ""),
        "official_status_en": STATUS_EN.get(row.get("verification_status", ""), row.get("verification_status", "")),
        "official_status_zh": row.get("verification_status", ""),
        "verification_status": row.get("verification_status", ""),
        "openness_level": "",
        "risk_level": infer_risk(row),
        "description_en": "",
        "description_zh": row.get("notes", ""),
        "source_dataset": "02-platforms.csv",
        "checked_at": row.get("checked_at", ""),
    }


def normalize_matrix_row(row: dict[str, str], idx: int) -> dict[str, str]:
    platform_en, platform_zh = split_platform(row["company"])
    domain_zh = row["industry"]
    status_zh = row.get("official_skill", "")
    return {
        "resource_id": f"aar-{idx:04d}",
        "platform_en": platform_en,
        "platform_zh": platform_zh,
        "product_or_resource": row.get("product_or_platform", ""),
        "domain_en": DOMAIN_EN.get(domain_zh, domain_zh),
        "domain_zh": domain_zh,
        "country_region": row.get("country_region", ""),
        "access_resource_types": resource_types(row),
        "official_cli": row.get("official_cli", ""),
        "official_skill": row.get("official_skill", ""),
        "official_mcp": "",
        "official_sdk_api": row.get("api_sdk_open", ""),
        "source_url": row.get("github_url", ""),
        "official_status_en": STATUS_EN.get(status_zh, status_zh),
        "official_status_zh": status_zh,
        "verification_status": status_zh,
        "openness_level": row.get("data_interface_openness", ""),
        "risk_level": infer_risk(row),
        "description_en": "",
        "description_zh": row.get("notes", ""),
        "source_dataset": "03-vendor-openness-matrix.csv",
        "checked_at": row.get("checked_at", ""),
    }


def normalize_ecosystem_row(row: dict[str, str], idx: int) -> dict[str, str]:
    platform_en, platform_zh = split_platform(row["company"])
    domain_zh = row["industry"]
    status_zh = row.get("status", "")
    return {
        "resource_id": f"aar-{idx:04d}",
        "platform_en": platform_en,
        "platform_zh": platform_zh,
        "product_or_resource": row.get("product", ""),
        "domain_en": DOMAIN_EN.get(domain_zh, domain_zh),
        "domain_zh": domain_zh,
        "country_region": row.get("country_region", ""),
        "access_resource_types": resource_types(row),
        "official_cli": row.get("cli_relevance", ""),
        "official_skill": status_zh,
        "official_mcp": "MCP" if "MCP" in row.get("skill_type", "") else "",
        "official_sdk_api": "API" if "API" in row.get("skill_type", "") else "",
        "source_url": row.get("github_url", ""),
        "official_status_en": STATUS_EN.get(status_zh, status_zh),
        "official_status_zh": status_zh,
        "verification_status": status_zh,
        "openness_level": "",
        "risk_level": infer_risk(row),
        "description_en": "",
        "description_zh": row.get("leading_reason", "") or row.get("notes", ""),
        "source_dataset": "04-agent-skill-ecosystem.csv",
        "checked_at": row.get("checked_at", ""),
    }


def main() -> None:
    output: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    candidates: list[tuple[dict[str, str], str]] = []
    for row in read_csv(DATA / "02-platforms.csv"):
        candidates.append((row, "platforms"))
    for row in read_csv(DATA / "03-vendor-openness-matrix.csv"):
        candidates.append((row, "matrix"))
    for row in read_csv(DATA / "04-agent-skill-ecosystem.csv"):
        candidates.append((row, "ecosystem"))

    for row, source in candidates:
        key = platform_key(row)
        if key in seen:
            continue
        seen.add(key)
        idx = len(output) + 1
        if source == "platforms":
            output.append(normalize_platform_row(row, idx))
        elif source == "matrix":
            output.append(normalize_matrix_row(row, idx))
        else:
            output.append(normalize_ecosystem_row(row, idx))

    with (DATA / "01-access-resources.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)

    print(f"wrote {len(output)} rows to data/01-access-resources.csv")


if __name__ == "__main__":
    main()
