<p align="center">
  <img src="assets/banner.svg" alt="Agent Access Entropy Index banner" width="100%">
</p>

# Agent Access Entropy Index

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-draft--index-blue)
![Data](https://img.shields.io/badge/data-CSV%20%2B%20Markdown-informational)

[English](README.md) | 中文

**Agent Access Entropy Index** 是一个由社区维护的“Agent 访问熵”索引，整理各类软件平台、数据供应商、金融终端、社交媒体、数字货币交易平台、云服务和开发者工具的官方来源 CLI、Agent Skill、MCP、SDK 与 API 访问路径。

它关注一个简单问题：

> 一个平台向 AI Agent 和开发者开放了多少可靠、官方来源、机器可读的访问路径？

## 快速使用

如果你想查询某个平台是否有官方 CLI、MCP、Agent Skill、SDK 或 API，可以直接使用主数据文件：

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

也可以用 SQLite 聚合某个行业的访问资源：

```bash
sqlite3 data/01-access-resources.sqlite \
  "SELECT domain_zh, access_resource_types, COUNT(*) FROM access_resources GROUP BY domain_zh, access_resource_types ORDER BY COUNT(*) DESC LIMIT 20;"
```

Agent 或自动化系统更适合读取 JSONL：

```bash
jq 'select(.domain_en == "Crypto trading") | {platform_en, access_resource_types, source_url}' data/01-access-resources.jsonl
```

如果你要持续追踪新的官方来源，可以维护 `data/05-tracked-entities.csv` 和 `data/06-tracking-watchlist.csv`，再运行：

```bash
python3 scripts/discover_candidates.py
python3 scripts/review_candidates.py
python3 scripts/sync_tracking_status.py
```

候选结果会进入 `data/09-candidates/`。这些是预审信号，不是已确认入库记录。

<!-- resource-stats:start -->
## 数据集概览

当前覆盖范围：

| 指标 | 数量 |
|---|---:|
| 访问资源 | 202 |
| 平台 / 软件 | 70 |
| 行业 / 领域 | 45 |

收录最多的领域：

- 数字货币交易: 39
- 金融数据与终端: 17
- 社交媒体: 14
- 云数据AI: 14
- 公有云与云原生: 13

数据集版本：`0.1.0`。
<!-- resource-stats:end -->

## 概念

**Agent 访问熵**描述一个平台面向 Agent 和开发者开放的官方来源访问路径的多样性与可靠性。

CLI、MCP、Agent Skill、SDK、API、Webhook、数据导出越丰富、越标准、越可自动化，访问熵越高；越封闭、越依赖人工界面、越缺少文档或只能依赖非官方封装，访问熵越低。

这个索引既可以用于单个平台，也可以用于行业层面：平台得分描述单个产品的访问熵，行业得分则聚合该领域多个重要平台的访问熵。

## 状态与免责声明

本项目是独立研究索引，不隶属于、不代表、不受任何已列厂商、平台、交易所、数据供应商、产品或 GitHub 组织赞助、认可或授权。

本仓库中使用的“官方”一词，仅表示来源看起来来自厂商官方 GitHub 组织、官方域名、官方文档或明确的产品团队。

本仓库只是索引，不是安全审计。详见 [免责声明](docs/11-disclaimer.md)。

## 收录内容

- 官方 CLI。
- 官方 Agent Skill 和 `SKILL.md` 仓库。
- 官方 MCP Server 和 MCP Plugin。
- 官方 SDK 和 API。
- 未发现官方入口时的社区补位项目。
- 官方来源证据与复核状态。
- 金融、数字货币、支付、交易、敏感数据等高风险场景说明。

## 数据文件

| 文件 | 说明 |
|---|---|
| [`data/01-access-resources.csv`](data/01-access-resources.csv) | 主统一表，用于按平台查询官方来源 access 资源。 |
| [`data/01-access-resources.jsonl`](data/01-access-resources.jsonl) | Agent 友好的 JSONL 导出，一行一个资源。 |
| [`data/01-access-resources.sqlite`](data/01-access-resources.sqlite) | 本地 SQLite 数据库，用于 SQL 查询和聚合。 |
| [`data/07-schema.json`](data/07-schema.json) | 统一 access resource 记录的 JSON Schema。 |
| [`data/08-manifest.json`](data/08-manifest.json) | 数据版本、行数、生成文件和校验和。 |
| [`data/02-platforms.csv`](data/02-platforms.csv) | 按平台/软件名反向检索，覆盖社交、办公、金融、数字货币、开发者平台、云、数据和 AI。 |
| [`data/03-vendor-openness-matrix.csv`](data/03-vendor-openness-matrix.csv) | 按行业整理官方 CLI、Skill、MCP、SDK、API 的开放性矩阵。 |
| [`data/04-agent-skill-ecosystem.csv`](data/04-agent-skill-ecosystem.csv) | 早期 Agent Skill 生态数据库。 |
| [`data/05-tracked-entities.csv`](data/05-tracked-entities.csv) | 被追踪的公司、平台、公共数据资源和专业软件基础表。 |
| [`data/06-tracking-watchlist.csv`](data/06-tracking-watchlist.csv) | 按实体关联的官方来源定时追踪清单。 |
| [`data/09-candidates/review-queue.md`](data/09-candidates/review-queue.md) | 从追踪来源生成的透明预审候选队列。 |

## 文档

| 文档 | 说明 |
|---|---|
| [反向平台审计](docs/06-reverse-platform-audit.md) | 按平台/软件名整理的可读审计表。 |
| [厂商开放性矩阵](docs/07-vendor-openness-matrix.md) | 行业开放性矩阵和观察。 |
| [官方 Skill/MCP 审计](docs/08-official-skill-mcp-audit.md) | 已确认官方 Skill/MCP 来源复核表。 |
| [Agent Skill 生态数据库](docs/09-agent-skill-ecosystem-database.md) | Agent Skill 生态笔记。 |
| [数据字典](docs/03-data-dictionary.md) | CSV 字段定义。 |
| [查询指南](docs/04-query-guide.md) | 如何查询 CSV、JSONL、SQLite 和 MCP tools。 |
| [候选追踪](docs/05-candidate-tracking.md) | 如何维护追踪实体、官方来源 watchlist、候选队列和入库状态。 |
| [方法论](docs/01-methodology.md) | 访问路径定义和评分草案。 |
| [官方来源判定规则](docs/02-verification-policy.md) | 官方、部分确认、社区、未确认的判定规则。 |
| [贡献指南](docs/10-contributing.md) | 贡献说明。 |
| [免责声明](docs/11-disclaimer.md) | 法律、安全、金融、商标等免责声明。 |

## 已确认官方来源示例

| 类别 | 平台 | 官方来源 |
|---|---|---|
| 开发者平台 | GitHub | [`cli/cli`](https://github.com/cli/cli), [`github/github-mcp-server`](https://github.com/github/github-mcp-server) |
| 办公协作 | 飞书 / Lark | [`larksuite/cli`](https://github.com/larksuite/cli) |
| 办公协作 | 钉钉 | [`DingTalk-Real-AI/dingtalk-workspace-cli`](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli) |
| 文档办公 | WPS / Kdocs | [`WPS-SmartDocs/WPS-AirPage-Skill`](https://github.com/WPS-SmartDocs/WPS-AirPage-Skill) |
| 知识库 | 语雀 | [`yuque/yuque-ecosystem`](https://github.com/yuque/yuque-ecosystem) |
| 金融数据 | Wind / 万得 | [`Wind-Information-Co-Ltd/wind-skills`](https://github.com/Wind-Information-Co-Ltd/wind-skills) |
| 金融数据 | 同花顺 iFinD | [iFinD MCP 平台](https://mcp.51ifind.com/) |
| 数字货币 | Binance / 币安 | [`binance/binance-skills-hub`](https://github.com/binance/binance-skills-hub) |
| 数字货币 | Coinbase | [`coinbase/agentic-wallet-skills`](https://github.com/coinbase/agentic-wallet-skills), [`coinbase/agentkit`](https://github.com/coinbase/agentkit), [`coinbase/payments-mcp`](https://github.com/coinbase/payments-mcp) |
| 数字货币 | OKX | [`okx/agent-skills`](https://github.com/okx/agent-skills), [`okx/agent-trade-kit`](https://github.com/okx/agent-trade-kit) |
| 数字货币 | Kraken | [`krakenfx/kraken-cli`](https://github.com/krakenfx/kraken-cli) |
| 数字货币市场数据 | CoinMarketCap | [`coinmarketcap-official/skills-for-ai-agents-by-CoinMarketCap`](https://github.com/coinmarketcap-official/skills-for-ai-agents-by-CoinMarketCap) |

## 评分草案

可以用现有 CSV 字段估算行业级 Agent 访问熵得分：

```text
Platform Entropy = Access × Velocity × Openness × Reliability
Industry Entropy = Σ Platform Entropy
Agent Access Entropy Index = 100 × Industry Entropy / MaxPossibleEntropy
```

建议解释：

| 分数 | 含义 |
|---:|---|
| 0-20 | 封闭或低机器访问 |
| 20-40 | 有限流动 |
| 40-60 | 中等流动 |
| 60-80 | 高流动 |
| 80-100 | 高速开放、机器可读的信息流动 |

风险应与开放度分开记录。数字货币交易、支付、账户变更、生产写入和链上签名即使是官方接口，也属于高风险能力。

## AI 友好访问

项目提供多种本地优先的数据格式：

```text
data/
  01-access-resources.csv
  01-access-resources.jsonl
  01-access-resources.sqlite
  07-schema.json
  08-manifest.json
```

`data/01-access-resources.csv` 是主数据。JSONL、SQLite、schema 和 manifest 都是由 CSV 生成的派生文件。

编辑 CSV 后，用下面命令重新生成派生文件：

```bash
python3 scripts/export_formats.py
```

该命令也会刷新中英文 README 中自动生成的资源数量统计区块。

如需 Agent 原生访问，可以运行 stdio MCP server：

```bash
python3 mcp/server.py
```

MCP tools 包括 `search_platform`、`list_access_resources`、`filter_by_resource_type`、`list_official_mcp` 和 `industry_summary`。

详见 [查询指南](docs/04-query-guide.md)。

## 候选追踪

定时追踪以 `data/05-tracked-entities.csv` 和 `data/06-tracking-watchlist.csv` 为基础。
发现流程会把透明候选产物写入 `data/09-candidates/`；这些只是预审信号，不是已确认入库记录。

本地运行：

```bash
python3 scripts/discover_candidates.py
python3 scripts/review_candidates.py
python3 scripts/sync_tracking_status.py
```

详见 [候选追踪](docs/05-candidate-tracking.md)。

## 版本管理

数据集/项目包版本记录在 [`VERSION`](VERSION)。变更记录见 [`CHANGELOG.md`](CHANGELOG.md)。

当前数据清单见 [`data/08-manifest.json`](data/08-manifest.json)，其中记录版本、行数、生成日期，以及主数据和派生数据文件的 SHA-256 校验和。

## 安全提示

被收录项目可能会执行命令、访问私有文件、调用外部服务、读写业务数据、触发支付、下单交易、转账数字货币或签署链上交易。

使用任何 CLI、Skill、MCP Server、Plugin、SDK 或脚本之前：

- 审查源代码和权限。
- 优先使用只读凭证。
- 尽量先使用沙盒或模拟交易环境。
- 不可逆操作必须人工确认。
- 不要把 API Key、钱包私钥和其他密钥暴露给 prompt 或日志。

## 贡献

欢迎提交修正和新增条目。新增条目请尽量提供官方来源 URL 和证据类型。

详见 [贡献指南](docs/10-contributing.md) 和 [官方来源判定规则](docs/02-verification-policy.md)。

## 安全

详见 [Security Policy](SECURITY.md)。如果发现恶意链接、冒充官方来源或不安全分类，请通过 GitHub issue 反馈。

## 许可证

MIT License。详见 [LICENSE](LICENSE)。
