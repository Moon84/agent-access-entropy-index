#!/usr/bin/env python3
"""Fill curated official tracking sources for entities that still need sources."""

from __future__ import annotations

import sqlite3
from datetime import date

from index_store import DB_PATH


CURATED_SOURCES = {
    "ent-bitget": {
        "homepage": "https://www.bitget.com/",
        "github": "https://github.com/BitgetLimited/v3-bitget-api-sdk",
        "docs": "https://www.bitget.com/api-doc/common/intro",
        "source_url": "https://www.bitget.com/api-doc/common/intro",
        "description_en": "Bitget provides crypto exchange API documentation and SDK connectors for trading integration.",
        "description_zh": "Bitget 提供数字货币交易所 API 文档和 SDK 连接器，用于交易集成。",
    },
    "ent-bitmex": {
        "homepage": "https://www.bitmex.com/",
        "github": "https://github.com/BitMEX/api-connectors",
        "docs": "https://www.bitmex.com/app/apiOverview",
        "source_url": "https://github.com/BitMEX/api-connectors",
        "description_en": "BitMEX provides cryptocurrency derivatives trading APIs and official API connector libraries.",
        "description_zh": "BitMEX 提供数字货币衍生品交易 API 和官方 API 连接器库。",
    },
    "ent-bybit": {
        "homepage": "https://www.bybit.com/",
        "github": "https://github.com/bybit-exchange/docs",
        "docs": "https://bybit-exchange.github.io/docs/v5/intro",
        "source_url": "https://github.com/bybit-exchange/docs",
        "description_en": "Bybit provides exchange API documentation and official SDK repositories for HTTP and WebSocket integration.",
        "description_zh": "Bybit 提供交易所 API 文档以及 HTTP 和 WebSocket 集成的官方 SDK 仓库。",
    },
    "ent-coingecko": {
        "homepage": "https://www.coingecko.com/",
        "github": "https://github.com/coingecko/coingecko-api-oas",
        "docs": "https://docs.coingecko.com/reference/introduction",
        "source_url": "https://github.com/coingecko/coingecko-api-oas",
        "description_en": "CoinGecko provides cryptocurrency market data APIs and an official OpenAPI specification.",
        "description_zh": "CoinGecko 提供数字货币市场数据 API 和官方 OpenAPI 规范。",
    },
    "ent-crypto-com": {
        "homepage": "https://crypto.com/exchange",
        "github": "https://github.com/crypto-com/crypto-exchange",
        "docs": "https://exchange-docs.crypto.com/exchange/v1/rest-ws/index.html",
        "source_url": "https://exchange-docs.crypto.com/exchange/v1/rest-ws/index.html",
        "description_en": "Crypto.com Exchange provides REST and WebSocket APIs for market data, account, and trading workflows.",
        "description_zh": "Crypto.com Exchange 提供用于行情、账户和交易流程的 REST 与 WebSocket API。",
    },
    "ent-debank": {
        "homepage": "https://debank.com/",
        "github": "",
        "docs": "https://docs.cloud.debank.com/",
        "source_url": "https://docs.cloud.debank.com/",
        "description_en": "DeBank Cloud provides OpenAPI access to DeFi chains, protocols, tokens, and user portfolio data.",
        "description_zh": "DeBank Cloud 提供面向 DeFi 链、协议、代币和用户投资组合数据的 OpenAPI。",
    },
    "ent-defillama": {
        "homepage": "https://defillama.com/",
        "github": "https://github.com/DefiLlama/api-docs",
        "docs": "https://defillama.com/docs/api",
        "source_url": "https://github.com/DefiLlama/api-docs",
        "description_en": "DefiLlama provides DeFi analytics and public API documentation for protocol and market data.",
        "description_zh": "DefiLlama 提供 DeFi 分析以及协议和市场数据的公开 API 文档。",
    },
    "ent-deribit": {
        "homepage": "https://www.deribit.com/",
        "github": "",
        "docs": "https://docs.deribit.com/",
        "source_url": "https://docs.deribit.com/",
        "description_en": "Deribit provides official API documentation for cryptocurrency futures, perpetuals, and options trading.",
        "description_zh": "Deribit 提供数字货币期货、永续合约和期权交易的官方 API 文档。",
    },
    "ent-gate-io": {
        "homepage": "https://www.gate.io/",
        "github": "https://github.com/gateio/rest-v4",
        "docs": "https://www.gate.io/docs/developers/apiv4/en/",
        "source_url": "https://github.com/gateio/rest-v4",
        "description_en": "Gate.io provides API v4 documentation and an official REST API repository for exchange integration.",
        "description_zh": "Gate.io 提供 API v4 文档和官方 REST API 仓库，用于交易所集成。",
    },
    "ent-instagram": {
        "homepage": "https://www.instagram.com/",
        "github": "",
        "docs": "https://developers.facebook.com/docs/instagram-platform/",
        "source_url": "https://developers.facebook.com/docs/instagram-platform/",
        "description_en": "Instagram is tracked through Meta developer documentation for Instagram Platform APIs and Graph API access.",
        "description_zh": "Instagram 通过 Meta 开发者文档中的 Instagram Platform API 和 Graph API 入口进行追踪。",
    },
    "ent-kucoin": {
        "homepage": "https://www.kucoin.com/",
        "github": "",
        "docs": "https://www.kucoin.com/docs-new",
        "source_url": "https://www.kucoin.com/docs-new",
        "description_en": "KuCoin provides official exchange API documentation for market data, account, and trading integration.",
        "description_zh": "KuCoin 提供用于行情、账户和交易集成的官方交易所 API 文档。",
    },
    "ent-moonpay": {
        "homepage": "https://www.moonpay.com/",
        "github": "https://github.com/moonpay/skills",
        "docs": "https://www.moonpay.com/agents",
        "source_url": "https://github.com/moonpay/skills",
        "description_en": "MoonPay provides public agent skills and developer entry points for crypto on-ramp and wallet workflows.",
        "description_zh": "MoonPay 提供面向加密资产出入金和钱包流程的公开 Agent Skill 与开发者入口。",
    },
    "ent-nethermind": {
        "homepage": "https://nethermind.io/",
        "github": "https://github.com/NethermindEth/nethermind",
        "docs": "https://docs.nethermind.io/",
        "source_url": "https://github.com/NethermindEth/nethermind",
        "description_en": "Nethermind provides an Ethereum execution client with public documentation and an official GitHub repository.",
        "description_zh": "Nethermind 提供以太坊执行客户端、公开文档和官方 GitHub 仓库。",
    },
    "ent-reddit": {
        "homepage": "https://www.reddit.com/",
        "github": "https://github.com/reddit/devvit-mcp",
        "docs": "https://developers.reddit.com/docs/",
        "source_url": "https://github.com/reddit/devvit-mcp",
        "description_en": "Reddit provides developer documentation, Devvit tooling, and an official MCP server for Devvit applications.",
        "description_zh": "Reddit 提供开发者文档、Devvit 工具以及用于 Devvit 应用的官方 MCP Server。",
    },
    "ent-tiktok": {
        "homepage": "https://www.tiktok.com/",
        "github": "https://github.com/tiktok/tiktok-research-api-wrapper",
        "docs": "https://developers.tiktok.com/doc/overview/",
        "source_url": "https://github.com/tiktok/tiktok-research-api-wrapper",
        "description_en": "TikTok provides developer platform documentation and an official Research API wrapper repository.",
        "description_zh": "TikTok 提供开发者平台文档和官方 Research API wrapper 仓库。",
    },
    "ent-uniswap": {
        "homepage": "https://uniswap.org/",
        "github": "https://github.com/Uniswap/docs",
        "docs": "https://docs.uniswap.org/",
        "source_url": "https://github.com/Uniswap/docs",
        "description_en": "Uniswap provides protocol documentation, SDK references, and official GitHub repositories for decentralized exchange integration.",
        "description_zh": "Uniswap 提供协议文档、SDK 参考和用于去中心化交易集成的官方 GitHub 仓库。",
    },
    "ent-wechat": {
        "homepage": "https://weixin.qq.com/",
        "github": "",
        "docs": "https://developers.weixin.qq.com/doc/",
        "source_url": "https://developers.weixin.qq.com/doc/",
        "description_en": "WeChat is tracked through Tencent's public developer documentation for mini programs, official accounts, and open platform APIs.",
        "description_zh": "微信通过腾讯公开开发者文档中的小程序、公众号和开放平台 API 入口进行追踪。",
    },
    "ent-wecom": {
        "homepage": "https://work.weixin.qq.com/",
        "github": "",
        "docs": "https://developer.work.weixin.qq.com/document",
        "source_url": "https://developer.work.weixin.qq.com/document",
        "description_en": "WeCom provides public developer documentation for enterprise messaging, apps, contacts, and integration APIs.",
        "description_zh": "企业微信提供面向企业消息、应用、通讯录和集成 API 的公开开发者文档。",
    },
}


def main() -> int:
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    try:
        for entity_id, source in CURATED_SOURCES.items():
            conn.execute(
                """
                UPDATE tracked_entities
                SET official_homepage = ?,
                    primary_github = ?,
                    primary_docs = ?,
                    tracking_status = CASE
                        WHEN tracking_status = 'needs_source' THEN 'needs_review'
                        ELSE tracking_status
                    END,
                    service_description_en = ?,
                    service_description_zh = ?,
                    checked_at = ?
                WHERE entity_id = ?
                """,
                (
                    source["homepage"],
                    source["github"],
                    source["docs"],
                    source["description_en"],
                    source["description_zh"],
                    today,
                    entity_id,
                ),
            )
            conn.execute(
                """
                UPDATE data_sources
                SET source_url = ?,
                    checked_at = ?
                WHERE (platform_en = (SELECT entity_name_en FROM tracked_entities WHERE entity_id = ?)
                    OR platform_zh = (SELECT entity_name_zh FROM tracked_entities WHERE entity_id = ?))
                    AND (source_url = '' OR lower(source_url) IN ('待补', 'todo', 'tbd', 'n/a', 'na', 'to be added'))
                """,
                (source["source_url"], today, entity_id, entity_id),
            )
        conn.commit()
    finally:
        conn.close()
    print(f"updated {len(CURATED_SOURCES)} tracked entities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
