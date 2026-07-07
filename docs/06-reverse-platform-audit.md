# 主流平台反向检索官方 Skill / CLI / MCP 审计表

更新日期：2026-07-06

## 1. 审计方法

本表从“平台/软件名称”反向检索，而不是从 Skill 仓库正向枚举。每个平台按以下关键词组合核验：

- `<平台名> skill`
- `<平台名> CLI`
- `<平台名> MCP`
- `<平台名> SKILL.md`
- `<平台名> official Agent Skills`
- `<平台名> GitHub official CLI`

判断优先级：

1. 官方公司/产品 GitHub 组织下的 Skill、CLI、MCP 仓库。
2. 官方文档或官方域名明确指向的 MCP/Skill/CLI。
3. 官方团队成员或产品核心维护者发布的准官方项目。
4. 社区项目，仅作为补位，不计入“官方来源”。

## 2. 总览

| 领域 | 官方 Skill/MCP/CLI 最明确的平台 | 官方缺位但社区活跃的平台 |
|---|---|---|
| 开发者平台 | GitHub, GitLab, Microsoft, Azure DevOps | Bitbucket 需继续查证 |
| 办公协作 | 飞书、钉钉、Kdocs/WPS、语雀、Google Workspace、Slack、Notion | 企业微信、腾讯文档需继续查证 |
| 金融数据 | Wind、iFinD、Bloomberg、LSEG、FactSet、Nasdaq Data Link | Choice、AKShare、Tushare、聚宽、米筐 |
| 数字货币/区块链交易 | Binance, OKX, Coinbase, Kraken, BNB Chain, CoinMarketCap | Bybit、Bitget、Gate、KuCoin 等多有 SDK/API，官方 Skill/MCP 需持续复核 |
| 社交媒体 | X API, Slack, Typefully, Taisly, Bright Data, Anysite | 小红书、Instagram、TikTok、YouTube、Reddit、微信公众号 |
| 云与开发者平台 | AWS, Azure, Firebase, Cloudflare, Vercel, Netlify, Supabase, 阿里云、腾讯云、火山引擎、华为云 | 部分云厂商已有 CLI 但 Skill 未显著公开 |
| 数据与数据库 | MongoDB, DuckDB, ClickHouse, Redis, Pinecone, Snowflake, Databricks | 国内数据库厂商官方 Skill 仍少 |
| AI/模型平台 | OpenAI, Anthropic, Hugging Face, MiniMax, 阿里云百炼, 来也 ADP | 部分模型厂商只提供 SDK/API |

## 3. 反向检索明细

### 3.1 社交媒体、内容平台与社区

| 平台/软件 | 官方 CLI | 官方 Skill | 官方 MCP | 官方来源地址 | 结论 | 检索关键词 |
|---|---|---|---|---|---|---|
| X / Twitter | 有，`xurl` | 未确认 | 未确认 | https://github.com/xdevplatform/xurl | 官方 CLI 生态明确；Agent Skill 多为第三方 | X API CLI, xurl official CLI, X MCP |
| Slack | 有 | Plugin 形态 | 有 hosted MCP / plugin | https://github.com/slackapi/slack-cli / https://github.com/slackapi/slack-mcp-plugin | 官方 CLI 与 MCP Plugin 已确认 | Slack CLI, Slack MCP plugin, slackapi |
| Typefully | 未确认 | 有官方 Skill | 未确认 | https://github.com/VoltAgent/awesome-agent-skills | 官方 Skill 在 Awesome Agent Skills 中收录 | Typefully skill, Typefully official skill |
| Taisly | 未确认 | 有 Agent Skill | 未确认 | https://github.com/taisly/agent | 社交媒体发布 Skill，官方来源需按 Taisly 组织核验 | Taisly social media posting skill |
| Bright Data | 有 CLI/MCP | 有 Skills | 有 MCP | https://github.com/brightdata/skills | 官方 Skills，覆盖 Web/Social 数据抽取 | Bright Data skills, Bright Data MCP |
| Anysite | 未确认 | 有官方 MCP Skills | 有 MCP | https://github.com/anysiteio/agent-skills | 官方 LinkedIn / social intelligence skills | Anysite MCP skills, LinkedIn intelligence |
| 小红书 | 未发现 | 未发现官方 | 未发现官方 | https://github.com/autoclaw-cc/xiaohongshu-skills | 官方缺位，社区 Skill 活跃 | 小红书 skill, xiaohongshu SKILL.md, 小红书 MCP |
| 微信公众号 | 未发现 | 未发现官方 | 未发现官方 | https://github.com/geekjourneyx/md2wechat-skill | 官方缺位，社区 md2wechat Skill/CLI 活跃 | 微信公众号 CLI, md2wechat skill |
| 微信 / WeChat | 未发现统一官方 CLI | 未发现官方 Skill | 未发现官方 MCP | 待补 | 官方接口分散在开放平台/公众号/企业微信 | WeChat MCP, 微信 SKILL.md |
| 企业微信 / WeCom | 未发现统一官方 CLI | 未发现官方 Skill | 未发现官方 MCP | 待补 | API 开放但官方 Agent Skill/MCP 需继续查证 | WeCom MCP, 企业微信 CLI |
| Instagram | 未发现官方 CLI | 未发现官方 Skill | 未发现官方 MCP | 待补 | Meta API 存在，但官方 Agent Skill/MCP 未确认 | Instagram MCP official, Instagram CLI |
| TikTok | 未发现官方 CLI | 未发现官方 Skill | 未发现官方 MCP | 待补 | TikTok API 存在，Agent Skill 多为第三方 | TikTok MCP official, TikTok CLI |
| YouTube | Google API/CLI 生态 | 未发现专属 Skill | 未确认专属 MCP | https://github.com/googleapis/google-api-python-client | API/SDK 官方成熟，专属 Agent Skill 未确认 | YouTube API CLI Skill MCP |
| Reddit | 未发现官方 CLI | 未发现官方 Skill | 未发现官方 MCP | 待补 | API 存在，MCP/Skill 多为社区 | Reddit MCP official |
| LinkedIn | 未发现官方 CLI | 未发现官方 Skill | 未发现官方 MCP | https://github.com/anysiteio/agent-skills | 官方 LinkedIn MCP 未确认；第三方 Anysite/Bright Data 覆盖 | LinkedIn MCP official, LinkedIn skill |

### 3.2 办公协作、文档与知识库

| 平台/软件 | 官方 CLI | 官方 Skill | 官方 MCP | 官方来源地址 | 结论 | 检索关键词 |
|---|---|---|---|---|---|---|
| Kdocs / 金山文档 / WPS 365 | 有，本地 CLI | 有 | 非典型 MCP | https://github.com/WPS-SmartDocs/WPS-AirPage-Skill | 官方 WPS AirPage Skill 已确认 | Kdocs skill, WPS AirPage Skill |
| 飞书 / Lark / Feishu | 有 | 有，20+ Agent Skills | CLI/命令网关形态 | https://github.com/larksuite/cli | 官方 CLI + Agent Skills 已确认 | Feishu CLI Agent Skills, larksuite cli |
| 钉钉 / DingTalk | 有 | 有 | 基于 MCP metadata/CLI | https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli | 官方 Workspace CLI 已确认 | DingTalk Workspace CLI skill MCP |
| 语雀 / Yuque | Plugin/MCP | 有 | 有 | https://github.com/yuque/yuque-ecosystem | 官方 MCP + Skills + Plugin 已确认 | Yuque MCP skills plugin |
| Google Workspace | 有，`gws` | 有 | 未确认独立 MCP | https://github.com/VoltAgent/awesome-agent-skills | 官方 Workspace CLI Skills 已确认 | Google Workspace CLI skills gws |
| Microsoft 365 / Microsoft Learn | 有 | 有 | 有 | https://github.com/MicrosoftDocs/mcp / https://github.com/microsoft/skills | Microsoft MCP/Skills 生态已确认 | Microsoft MCP skills Microsoft 365 |
| Notion | 未确认官方 CLI | Plugin/Skill 形态 | 有官方 MCP | https://github.com/makenotion/notion-mcp-server | 官方 Notion MCP Server 已确认 | Notion MCP server official |
| Slack | 有 | Plugin 形态 | 有 | https://github.com/slackapi/slack-mcp-plugin | 官方 MCP Plugin 已确认 | Slack MCP official |
| Obsidian | 生态 CLI | 准官方 | 未确认官方 MCP | https://github.com/kepano/obsidian-skills | CEO 发布 Agent Skills，准官方 | Obsidian skills kepano |
| Zotero | 未发现官方 CLI | 未发现官方 Skill | 未发现官方 MCP | https://github.com/zotero/zotero | 官方 Skill/MCP 缺位，社区 CLI 补位 | Zotero CLI skill MCP |
| 腾讯文档 | 未发现 | 未发现 | 未发现 | 待补 | API/开放平台线索不足 | 腾讯文档 CLI Skill MCP |
| 石墨文档 | 未发现 | 未发现 | 未发现 | 待补 | 未发现官方 Agent 入口 | 石墨文档 MCP Skill |

### 3.3 金融数据、行情终端与投研平台

| 平台/软件 | 官方 CLI | 官方 Skill | 官方 MCP | 官方来源地址 | 结论 | 检索关键词 |
|---|---|---|---|---|---|---|
| Wind / 万得 | Skill 内置 CLI 调用 | 有 | 有，`wind-mcp-skill` | https://github.com/Wind-Information-Co-Ltd/wind-skills | 官方 Skill/MCP Skill 已确认 | Wind skill MCP wind-skills |
| Wind AIFinMarket | API Key/平台 | 相关 | 相关 | https://aifinmarket.wind.com.cn/#/home | Wind Skills 依赖 API Key | Wind AIFinMarket API Key |
| 同花顺 iFinD | MCP 平台/Token | 未确认 GitHub Skill | 有官方 MCP 平台 | https://mcp.51ifind.com/ | 官方 MCP 平台已确认，GitHub Skill 未确认 | iFinD MCP official |
| 东方财富 Choice | 未发现 | 未发现 | 未发现 | https://choice.eastmoney.com | 终端/API 存在，但官方 Skill/MCP 未发现 | Choice MCP Skill 东方财富 |
| Bloomberg | Terminal/API | 未发现官方 Skill | 未发现官方 MCP | https://github.com/msitt/blpapi-python | API 成熟，MCP/Skill 未确认官方 | Bloomberg MCP BLPAPI Skill |
| LSEG / Refinitiv | SDK/API | 未发现 | 未发现 | https://github.com/LSEG-API-Samples/Example.DataLibrary.Python | 官方 SDK 样例明确，Skill/MCP 未确认 | LSEG MCP Data Library |
| FactSet | SDK/API | 未发现 | 未发现 | https://github.com/factset | 官方 SDK GitHub 组织明确，Skill/MCP 未确认 | FactSet MCP Skill |
| Morningstar | API/Direct | 未发现 | 未发现 | https://developer.morningstar.com | 商业授权 API，未发现 Skill/MCP | Morningstar MCP Skill |
| S&P Global / Capital IQ | API | 未发现 | 未发现 | https://developer.spglobal.com | 商业授权 API，未发现 Skill/MCP | Capital IQ MCP Skill |
| Nasdaq Data Link | SDK/API | 未发现 | 未发现 | https://github.com/Nasdaq/data-link-python | 官方 Python SDK 明确 | Nasdaq Data Link MCP Skill |
| Polygon.io / Massive | SDK/API | 未发现 | 未发现 | https://github.com/massive-com/client-python | 官方 Python client 明确 | Polygon MCP Massive Skill |
| Alpaca | SDK/API | 未发现 | 未发现 | https://github.com/alpacahq/alpaca-py | 交易/行情 API 官方 SDK 明确 | Alpaca MCP Skill |
| Interactive Brokers | TWS/API | 未发现 | 未发现 | https://github.com/InteractiveBrokers/tws-api-public | API 明确，交易自动化需风控 | IBKR MCP Skill |
| Tushare Pro | SDK/API | Wind 仓库中有 Tushare Skill | 未确认 | https://github.com/waditu/tushare / https://github.com/Wind-Information-Co-Ltd/wind-skills | Tushare 官方 Skill 未确认，Wind 仓库收录相关 Skill | Tushare skill MCP |
| AKShare | Python SDK | 非官方/本地 Skill 可用 | 社区 MCP | https://github.com/akfamily/akshare | 开源 SDK 强，官方 Agent Skill 未确认 | AKShare MCP Skill |
| 聚宽 JoinQuant | SDK/API | 未发现 | 未发现 | https://www.joinquant.com | 平台内 API 为主，Agent 入口未确认 | JoinQuant MCP Skill |
| 米筐 Ricequant | SDK/API | 未发现 | 未发现 | https://www.ricequant.com | 平台内 API 为主，Agent 入口未确认 | Ricequant MCP Skill |

### 3.4 数字货币、比特币交易平台与链上基础设施

| 平台/软件 | 官方 CLI | 官方 Skill | 官方 MCP | 官方来源地址 | 结论 | 检索关键词 |
|---|---|---|---|---|---|---|
| Binance / 币安 | CLI/Skill hub 内工具 | 有，`binance-skills-hub` | 未确认官方 MCP；社区 MCP 多 | https://github.com/binance/binance-skills-hub | 官方 Skills Hub 已确认，面向 crypto 原生 Agent 能力 | Binance skills hub, Binance SKILL.md, Binance MCP |
| BNB Chain | MCP 相关工具 | 有，`bnbchain-skills` | 有 BNB Chain MCP 指引 | https://github.com/bnb-chain/bnbchain-skills | 官方 BNB Chain Skills 已确认，指导 Agent 使用 BNB Chain MCP | BNB Chain skills MCP |
| Coinbase | `awal` / AgentKit 工具链 | 有，`agentic-wallet-skills` | 有，`payments-mcp`；AgentKit 含 MCP 示例 | https://github.com/coinbase/agentic-wallet-skills / https://github.com/coinbase/payments-mcp / https://github.com/coinbase/agentkit | 官方 Skill、AgentKit、Payments MCP 均已确认 | Coinbase agentic wallet skills, Coinbase payments MCP, AgentKit MCP |
| Base | AgentKit/Base MCP 生态 | 有相关 Agent skills | 有，Base MCP legacy | https://github.com/base/base-mcp-legacy / https://github.com/coinbase/agentkit | Coinbase/Base 链上 Agent 生态明确 | Base MCP Coinbase AgentKit |
| OKX | 有，`@okx_ai/okx-trade-cli` | 有，`okx/agent-skills` | 有，`okx/agent-trade-kit` | https://github.com/okx/agent-skills / https://github.com/okx/agent-trade-kit | 官方 Skill + MCP trading kit 已确认 | OKX agent skills, OKX agent trade kit, OKX MCP |
| Kraken | 有，`kraken-cli` | CLI 内置 Agent 场景；未确认独立 Skill 仓库 | CLI 内置 MCP server | https://github.com/krakenfx/kraken-cli | 官方 AI-native CLI 已确认，支持 crypto/stocks/forex/derivatives 与 MCP server | Kraken CLI MCP AI-native |
| CoinMarketCap | API Skills | 有，`skills-for-ai-agents-by-CoinMarketCap` | Skill 形式支持 MCP Skills | https://github.com/coinmarketcap-official/skills-for-ai-agents-by-CoinMarketCap | 官方 CoinMarketCap Skills 已确认 | CoinMarketCap skills for AI agents |
| Uniswap | SDK/API | 官方 Skill 线索需复核源仓 | 未确认官方 MCP | 待补 | DEX 头部平台，官方 SDK/API 成熟；Skill/MCP 官方源需复核 | Uniswap official skill MCP |
| MoonPay | SDK/API | 官方 Skill 线索需复核源仓 | 未确认官方 MCP | 待补 | 法币出入金平台，需继续确认官方 Agent 入口 | MoonPay official skill MCP |
| Nethermind | SDK/节点工具 | 官方 Skill 线索需复核源仓 | 未确认官方 MCP | 待补 | 区块链基础设施/客户端，需继续确认 Skill/MCP | Nethermind skill MCP |
| Bybit | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 待补 | 常见第三方 SDK/API，未确认官方 Agent Skill/MCP | Bybit MCP Skill official |
| Bitget | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 待补 | 官方 API 存在，Agent Skill/MCP 多需继续查证 | Bitget MCP Skill official |
| Gate.io | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 待补 | 官方 API 存在，Agent Skill/MCP 未确认 | Gate.io MCP Skill official |
| KuCoin | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 待补 | 官方 API 存在，Agent Skill/MCP 未确认 | KuCoin MCP Skill official |
| Crypto.com | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 待补 | 交易平台 API 存在，Agent Skill/MCP 未确认 | Crypto.com MCP Skill official |
| BitMEX | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 待补 | API/交易接口成熟，Agent Skill/MCP 未确认 | BitMEX MCP Skill official |
| Deribit | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 待补 | 期权/衍生品 API 成熟，Agent Skill/MCP 未确认 | Deribit MCP Skill official |
| CoinGecko | API/SDK | 未确认官方 Skill | CoinGecko MCP 线索需复核 | 待补 | 价格/市场数据平台，MCP/Skill 需确认官方源 | CoinGecko MCP official |
| DeBank | API/数据平台 | 未确认官方 Skill | 未确认官方 MCP | 待补 | 链上资产/钱包数据平台，官方 Agent 入口未确认 | DeBank MCP Skill official |
| DefiLlama | API/数据平台 | 未确认官方 Skill | 未确认官方 MCP | 待补 | DeFi 数据 API 开放，Agent 入口多为社区 | DefiLlama MCP Skill |

风险提示：

- 数字货币平台的 Skill/MCP 往往可触发真实交易、转账、授权和链上签名。即便是官方项目，也应默认要求人工确认、额度限制、只读模式优先、密钥隔离和审计日志。
- “行情/研究/查询”与“交易/转账/授权”应分开分级。用于审计或研究时，建议优先选择只读 API Key 和 paper trading / sandbox。
- 社区 MCP/Skill 数量很多，但交易类社区项目不应默认信任，必须检查代码、权限、私钥处理方式和订单执行路径。

### 3.5 开发者平台、代码托管与工程协作

| 平台/软件 | 官方 CLI | 官方 Skill | 官方 MCP | 官方来源地址 | 结论 | 检索关键词 |
|---|---|---|---|---|---|---|
| GitHub | 有，`gh` | 有，`cli/cli` 的 `gh` Skill | 有 | https://github.com/cli/cli / https://github.com/github/github-mcp-server | 官方 CLI、Skill、MCP 均确认 | GitHub CLI skill MCP |
| GitLab | 有，`glab` | 未确认 | 未确认 | https://gitlab.com/gitlab-org/cli | 官方 CLI 确认；Skill/MCP 待查 | GitLab CLI skill MCP |
| Azure DevOps | 有扩展 | Microsoft Skill/MCP 生态 | Microsoft MCP | https://github.com/microsoft/azure-devops-cli-extension / https://github.com/microsoft/skills | Microsoft 生态确认，Azure DevOps 专属 Skill 需细查 | Azure DevOps MCP skill |
| Bitbucket | 未确认统一官方 CLI | 未确认 | 未确认 | 待补 | Atlassian API 存在，官方 Agent 入口需查 | Bitbucket CLI MCP Skill |
| Jira / Confluence | Atlassian CLI/API 生态 | Claude official plugins 线索 | 未确认官方 GitHub MCP | 待补 | 常见于官方插件/第三方 MCP，GitHub 官方源需核验 | Atlassian MCP Jira Confluence |

### 3.6 云、数据库、AI 与数据基础设施

| 平台/软件 | 官方 CLI | 官方 Skill | 官方 MCP | 官方来源地址 | 结论 | 检索关键词 |
|---|---|---|---|---|---|---|
| AWS | 有 | 未确认官方 Skill | 未确认官方 MCP | https://github.com/aws/aws-cli | 官方 CLI 明确，Skill/MCP 未确认官方 | AWS CLI MCP Skill |
| Azure | 有 | 有 Microsoft Skills | 有 Microsoft MCP | https://github.com/Azure/azure-cli / https://github.com/microsoft/skills | 官方 CLI + Skills/MCP 生态明确 | Azure CLI skills MCP |
| Google Cloud | 有 | 有 Skill | 未确认独立 MCP | https://github.com/VoltAgent/awesome-agent-skills | 官方 Skill 在聚合库确认 | Google Cloud skill gcloud |
| Cloudflare | 有 Wrangler | 有 | 未确认 | https://github.com/cloudflare/workers-sdk | 官方 CLI + Skills 确认 | Cloudflare Wrangler skill |
| Vercel | 有 | 有 | 未确认 | https://github.com/vercel/vercel / https://github.com/vercel-labs/skills | 官方/实验室 Skills 确认 | Vercel skill CLI |
| Netlify | 有 | 有 | 未确认 | https://github.com/netlify/cli | 官方 CLI + Skills 确认 | Netlify CLI skill |
| Supabase | 有 | 有 | 有 hosted/平台 MCP 线索 | https://github.com/supabase/cli | 官方 CLI 明确，MCP 需按平台文档继续查 | Supabase CLI MCP Skill |
| MongoDB | 有 mongosh | 有 | 未确认 | https://github.com/mongodb-js/mongosh | 官方 CLI + Skills 收录 | MongoDB skill mongosh |
| DuckDB | 有 | 有 | 未确认 | https://github.com/duckdb/duckdb | 官方 CLI + Skills 收录 | DuckDB skill CLI |
| ClickHouse | 有 | 有 | 未确认 | https://github.com/ClickHouse/ClickHouse | 官方 Skills 收录 | ClickHouse skill CLI |
| Redis | 有 | 有 | 未确认 | https://github.com/redis/redis | 官方 Skills 收录 | Redis skill MCP |
| Pinecone | SDK/API | 有 | 未确认 | https://github.com/pinecone-io/skills | 官方 Agent Skills library 确认 | Pinecone skills MCP |
| OpenAI | SDK/API | 有 | 未确认官方 MCP | https://github.com/openai/openai-python | 官方 SDK + Codex Skill 生态 | OpenAI skill MCP |
| Anthropic | SDK/API | 有 | MCP 生态核心方 | https://github.com/anthropics/anthropic-sdk-python | 官方 Claude Skills 生态 | Anthropic skills MCP |
| Hugging Face | 有 `hf` | 有 | 未确认 | https://github.com/huggingface/huggingface_hub | 官方 CLI/SDK + Skills 确认 | Hugging Face hf-cli skill |
| MiniMax | CLI/API | 有 | 未确认 | https://github.com/VoltAgent/awesome-agent-skills | 官方 Skill 收录 | MiniMax skill CLI |
| 阿里云百炼 Model Studio | 有 | 未确认 | 未确认 | https://github.com/modelstudioai/cli | Agent-first CLI 明确 | Model Studio CLI skill |
| 来也 ADP | 有 | 有 | 未确认 | https://github.com/laiye-ai/adp-cli | 官方 CLI + Skill 明确 | Laiye ADP CLI skill |

## 4. 可直接写入主矩阵的修正点

| 项目 | 修正 |
|---|---|
| Wind | 从“未发现官方 Skill”修正为“有官方 Skill/MCP Skill”，地址为 https://github.com/Wind-Information-Co-Ltd/wind-skills |
| iFinD | 从“未发现官方”修正为“有官方 MCP 平台；未确认官方 GitHub Skill”，地址为 https://mcp.51ifind.com/ |
| Notion | 增加“官方 MCP Server”，地址为 https://github.com/makenotion/notion-mcp-server |
| Slack | 增加“官方 MCP Plugin”，地址为 https://github.com/slackapi/slack-mcp-plugin |
| GitHub | 增加“官方 MCP Server”，地址为 https://github.com/github/github-mcp-server |
| Microsoft | 增加 `microsoft/skills`，地址为 https://github.com/microsoft/skills |
| Kdocs/WPS | 保持“官方 Skill”，地址为 https://github.com/WPS-SmartDocs/WPS-AirPage-Skill |
| Binance | 增加官方 Skills Hub，地址为 https://github.com/binance/binance-skills-hub |
| Coinbase | 增加官方 Agentic Wallet Skills、AgentKit、Payments MCP，地址为 https://github.com/coinbase/agentic-wallet-skills、https://github.com/coinbase/agentkit、https://github.com/coinbase/payments-mcp |
| OKX | 增加官方 Agent Skills 与 Agent Trade Kit，地址为 https://github.com/okx/agent-skills、https://github.com/okx/agent-trade-kit |
| Kraken | 增加官方 AI-native CLI / MCP server，地址为 https://github.com/krakenfx/kraken-cli |
| CoinMarketCap | 增加官方 AI Agent Skills，地址为 https://github.com/coinmarketcap-official/skills-for-ai-agents-by-CoinMarketCap |
