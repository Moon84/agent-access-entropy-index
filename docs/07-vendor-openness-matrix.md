# 官方 CLI / Agent Skill / 数据接口开放性对照数据库

更新日期：2026-07-06

## 1. 方法与口径

本次整理按用户要求调用已安装的 GitHub 官方 `gh` Skill，并按其建议优先使用结构化输出方式检索 GitHub：

- 已读取本机安装的 `~/.copilot/skills/gh/SKILL.md`。
- 尝试使用 `gh search repos --json ...` 搜索官方 CLI 与 Agent Skill。
- 当前 `gh` 未登录，`gh search` 返回需要 `gh auth login` 或 `GH_TOKEN`。
- 随后使用 GitHub 公共 REST API、GitHub 仓库页面与此前已验证仓库数据补齐。

### 字段说明

| 字段 | 说明 |
|---|---|
| 官方 CLI | 公司或官方组织维护的命令行工具 |
| 官方 Skill | 官方 Agent Skill、Skill library、Plugin，或官方 CLI 自带 Skill |
| API/SDK 开放性 | 是否提供公开 API、SDK、OpenAPI、GraphQL、REST 等 |
| 数据/接口开放性 | 综合判断：高 / 中高 / 中 / 低 / 未发现 |
| GitHub 地址 | 优先给官方 GitHub 仓库；若官方 Skill 来源在聚合库中，则给可追踪入口 |

### 开放性等级

| 等级 | 判断标准 |
|---|---|
| 高 | 官方 CLI + 官方 API/SDK + 较完整文档，适合 Agent 自动化 |
| 中高 | 官方 API/SDK 完整，CLI 或 Skill 缺一项 |
| 中 | API 存在但能力、权限、速率、数据范围受限，或 Skill 主要由社区提供 |
| 低 | 平台领先但官方 CLI/Skill/API 开放弱，自动化主要靠社区或非正式方案 |
| 未发现 | 暂未发现官方 CLI、Skill 或公开可用接口 |

## 2. 总览结论

| 行业 | 开放性最高的代表 | 中国重点 | 主要缺口 |
|---|---|---|---|
| 开发者平台与代码托管 | GitHub | Gitee 需进一步验证 | 官方 Skill 正在出现，GitHub 领先 |
| 公有云与云原生 | AWS, Azure, Cloudflare, Alibaba Cloud, Tencent Cloud, Volcengine | 阿里云、腾讯云、火山引擎、华为云 | 华为云 Skill 明确，但 CLI 侧需继续查证官方主仓 |
| 企业协作与办公 | Google Workspace CLI, Slack, Notion | 飞书、钉钉、金山文档、语雀 | 国内协作平台反而在 Agent Skill 上推进很快 |
| 支付、电商与 CRM | Stripe, Shopify, Salesforce, Twilio | 暂未发现同等成熟中国官方 Skill | API 开放成熟，但 Skill 化程度不一 |
| 数据平台与数据库 | Snowflake, Databricks, dbt, MongoDB, DuckDB, ClickHouse, Redis | 中国数据库厂商官方 Skill 暂未明显进入 | 数据库 CLI 多，Agent Skill 仍早期 |
| 数据供应商 | Kaggle, IPinfo, Massive | 微信读书社区 CLI、中文平台 API 较少 | 平台数据开放性差异极大 |
| 金融数据、行情终端与研究平台 | Bloomberg, LSEG, FactSet, Wind, Choice, iFinD | Wind、Choice、同花顺 iFinD、聚宽、米筐、Tushare Pro | Wind 已有官方 Skill；iFinD 有官方 MCP 平台；多数金融终端仍以商业授权 API 为主 |
| 数字货币/比特币交易平台 | Binance, Coinbase, OKX, Kraken, CoinMarketCap | Binance、OKX | Bybit、Bitget、Gate、KuCoin 等需继续确认官方 Skill/MCP |
| AI / 模型平台 | OpenAI, Anthropic, Hugging Face, Pinecone | MiniMax, 阿里云百炼 Model Studio, 来也 ADP | 国内模型平台开始出现 Agent-first CLI |
| 知识管理与科研 | Obsidian, Zotero | 语雀、金山文档 | Zotero 官方 Skill 缺位 |
| 社交与内容平台 | X API 生态、Typefully | 小红书、微信公众号 | 小红书/微信官方 Skill 缺位，社区先行 |

## 3. 行业领先厂商开放性矩阵

### 3.1 开发者平台与代码托管

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| GitHub | 有，`gh` | 有，`cli/cli` 内置 `gh` Skill | 高 | 高 | https://github.com/cli/cli | GitHub 官方 CLI；已安装 `gh` Skill 到本机 `~/.copilot/skills/gh` |
| GitLab | 有，`glab`，但主维护迁至 GitLab.com | 未在 GitHub 发现官方 Skill | 高 | 中高 | https://github.com/profclems/glab | GitHub 仓库已归档，说明已被 GitLab 官方采纳并迁移维护 |
| Bitbucket / Atlassian | 未发现统一官方 CLI | 未发现官方 Skill | 中高 | 中 | 待补 | Atlassian Cloud API 完整，但官方 CLI/Skill 需进一步查证 |

### 3.2 公有云、云原生与部署平台

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| AWS | 有，AWS CLI | 未发现官方 Agent Skill | 高 | 高 | https://github.com/aws/aws-cli | AWS 通用命令行工具，云 API 开放度最高梯队 |
| Azure | 有，Azure CLI | Microsoft 有官方 Skill/MCP 生态 | 高 | 高 | https://github.com/Azure/azure-cli | Azure 官方 CLI；Microsoft 另有 Learn MCP/Skill 生态 |
| Google Cloud | 有，gcloud | 有 Google Cloud Skills | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | gcloud 官方 CLI 存在，但本次未确认官方 GitHub 源码主仓 |
| Firebase | 有 | 有官方 Skill | 高 | 高 | https://github.com/firebase/firebase-tools | Firebase CLI 覆盖 Hosting、Functions、Firestore 等 |
| Cloudflare | 有，Wrangler | 有官方 Skill | 高 | 高 | https://github.com/cloudflare/workers-sdk | Workers SDK 仓库包含 Wrangler，Skill 覆盖 Workers、R2、D1、KV |
| Vercel | 有 | 有官方 Skill | 高 | 高 | https://github.com/vercel/vercel | Vercel CLI 与 Next.js 平台能力开放成熟 |
| Netlify | 有 | 有官方 Skill | 高 | 高 | https://github.com/netlify/cli | Netlify CLI，官方 Skill 覆盖 deploy、functions、edge |
| Supabase | 有 | 有官方 Skill | 高 | 高 | https://github.com/supabase/cli | 本地开发、迁移、Edge Functions、类型生成 |
| Neon | 有 | 有官方 Skill | 中高 | 中高 | https://github.com/neondatabase/neonctl | Serverless Postgres CLI |
| HashiCorp Terraform | 有 | 有官方 Skill | 高 | 高 | https://github.com/hashicorp/terraform | 通过 provider 将云 API 声明式化 |
| Alibaba Cloud / 阿里云 | 有 | 未发现官方 Skill | 高 | 高 | https://github.com/aliyun/aliyun-cli | Alibaba Cloud CLI 基于 OpenAPI 管理云资源 |
| Tencent Cloud / 腾讯云 | 有 | 未发现官方 Skill | 高 | 高 | https://github.com/TencentCloud/tencentcloud-cli | TCCLI 调用腾讯云 API 3.0，支持自动化脚本 |
| Huawei Cloud / 华为云 | 待补 | 有官方 Agent Skills | 高 | 中高 | https://github.com/huaweicloud/huaweicloud-skills | 官方 Huawei Cloud Agent Skills，CLI 主仓需继续核验 |
| Volcengine / 火山引擎 | 有 | 未发现官方 Skill | 高 | 高 | https://github.com/volcengine/volcengine-cli | `ve` CLI 调用和管理火山引擎 OpenAPI |

### 3.3 企业协作、办公与知识库

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| Google Workspace | 有，`gws` | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | Drive、Sheets、Gmail、Calendar、Docs、Slides 等 |
| Microsoft 365 / Learn | 有多 CLI 与 MCP | 有 Microsoft Skills/MCP | 高 | 高 | https://github.com/MicrosoftDocs/mcp | Microsoft Learn MCP Server and CLI，另有 Azure CLI |
| Slack | 有 | 未发现官方 Skill | 高 | 中高 | https://github.com/slackapi/slack-cli | Slack app 创建、开发与部署 CLI |
| Notion | 未发现官方 CLI | 有官方 Skill | 中高 | 中高 | https://github.com/VoltAgent/awesome-agent-skills | API 开放较好，Skill 覆盖页面与数据库工作流 |
| 飞书 / Lark / Feishu | 有 | 有，CLI 自带 Agent Skills | 高 | 高 | https://github.com/larksuite/cli | 官方 Lark/Feishu CLI，200+ commands，20+ Agent Skills |
| 钉钉 / DingTalk | 有 | 有，CLI 面向 Agent 场景 | 高 | 高 | https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli | 官方开源跨平台 CLI，统一钉钉产品能力 |
| 金山文档 / WPS 365 | 有，本地 CLI | 有 | 中高 | 中高 | https://github.com/WPS-SmartDocs/WPS-AirPage-Skill | WPS 365 AirPage Skill，可创建文档、编辑块、表格、图片、评论 |
| 语雀 / Yuque | 通过 MCP/Plugin | 有 | 中高 | 中高 | https://github.com/yuque/yuque-ecosystem | MCP Server、Skills、Plugin 组合，知识库搜索与写作 |
| Obsidian | Obsidian CLI 生态 | 准官方 | 高，本地文件开放 | 高 | https://github.com/kepano/obsidian-skills | 由 Obsidian CEO 发布，面向 Markdown、Bases、JSON Canvas |
| Zotero | 未发现官方 CLI | 未发现官方 Skill | 中高 | 中 | https://github.com/zotero/zotero | 主产品开源且 API 存在，Skill 主要由社区补位 |

### 3.4 支付、电商、CRM 与通信 API

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| Stripe | 有 | 有官方 Skill | 高 | 高 | https://github.com/stripe/stripe-cli | 支付 API、Webhook、本地开发体验成熟 |
| Shopify | 有 | 未发现官方 Skill | 高 | 高 | https://github.com/Shopify/cli | App、Theme、Hydrogen storefront 开发 |
| Salesforce | 有，`sf` | 未发现官方 Agent Skill | 高 | 中高 | https://github.com/salesforcecli/cli | CRM 平台 CLI，企业权限与对象模型复杂 |
| Twilio | 有 | 未发现官方 Skill | 高 | 高 | https://github.com/twilio/twilio-cli | 通信 API CLI，短信、语音、验证等 |
| Auth0 | 官方 CLI/API 生态 | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | 身份认证、授权与用户管理 |
| Resend | 有 | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | 邮件 API 与 CLI 工作流 |

### 3.5 数据平台、数据库与分析

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| Snowflake | 有 | 未发现官方 Skill | 高 | 中高 | https://github.com/snowflakedb/snowflake-cli | Snowflake CLI 面向开发者工作流与 SQL 操作 |
| Databricks | 有 | 未发现官方 Skill | 高 | 中高 | https://github.com/databricks/cli | Databricks CLI，适合 Jobs、Workspace、Lakehouse 自动化 |
| dbt Labs | 有，dbt Core | 未发现官方 Agent Skill | 高 | 高 | https://github.com/dbt-labs/dbt-core | 数据转换事实标准，适合 Agent 生成/检查 SQL 模型 |
| MongoDB | 有，mongosh | 有官方 Skill | 高 | 高 | https://github.com/mongodb-js/mongosh | MongoDB Shell，官方 Skill 生态已出现 |
| ClickHouse | 有 | 有官方 Skill | 高 | 高 | https://github.com/ClickHouse/ClickHouse | 实时分析数据库，官方 Skill 覆盖查询与数据分析 |
| DuckDB | 有 | 有官方 Skill | 高 | 高 | https://github.com/duckdb/duckdb | 本地分析数据库，Agent 调用很友好 |
| Redis | 有 | 有官方 Skill | 高 | 高 | https://github.com/redis/redis | 缓存、数据结构、向量查询等能力 |
| Tinybird | 有 | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | 实时数据 API、SQL、数据管道 |
| Pinecone | API/SDK | 有官方 Agent Skills | 高 | 高 | https://github.com/pinecone-io/skills | 向量数据库，官方 Agent Skills library |

### 3.6 数据供应商与数据市场

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| Kaggle | 有 | 未发现官方 Skill | 高 | 高 | https://github.com/Kaggle/kaggle-cli | 官方 Kaggle CLI，数据集和竞赛数据开放度高 |
| IPinfo | 有 | 未发现官方 Skill | 高 | 高 | https://github.com/ipinfo/cli | IP 地理位置与网络数据 CLI |
| Massive / Polygon.io | SDK | 未发现官方 Skill | 高 | 中高 | https://github.com/massive-com/client-python | 金融市场 REST/WebSocket API 官方 Python client |
| X API | xurl CLI 生态 | 未发现官方 Skill | 中高 | 中 | https://github.com/xdevplatform/xurl | X API CLI；数据访问受 API 权限和定价影响 |
| SEC EDGAR | 无统一官方 CLI | 未发现 Skill | 高 | 高 | 待补 | 监管数据开放，但通常通过 API/下载接口使用 |
| 小红书 | 未发现官方 CLI | 未发现官方 Skill | 低 | 低 | https://github.com/autoclaw-cc/xiaohongshu-skills | 社区 Skill 活跃，但平台官方开放性弱 |
| 微信公众号 | 未发现官方 CLI | 未发现官方 Skill | 中 | 中 | https://github.com/geekjourneyx/md2wechat-skill | 社区 Markdown 发布 CLI 领先，官方接口限制较多 |
| 微信读书 | 社区 CLI | 未发现官方 Skill | 中 | 中 | https://github.com/shiquda/weread-cli | 社区基于官方支持 API 的 CLI，适合笔记/划线场景 |

### 3.7 金融数据、行情终端与研究平台

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| Wind / 万得 | Skill 内置 CLI 调用 | 有官方 Skill / MCP Skill | 高，商业授权 | 高 | https://github.com/Wind-Information-Co-Ltd/wind-skills | 官方 wind-skills monorepo，包含 wind-mcp-skill、wind-find-finance-skill、wind-alice 等；通过 Wind AIFinMarket API Key 接入 |
| 东方财富 Choice | 未发现官方 CLI | 未发现官方 Skill/MCP | 中高，商业授权 | 中 | https://choice.eastmoney.com | Choice 金融终端有 Choice 数据库、Choice 量化接口等，但未发现官方 Agent Skill/MCP 公开入口 |
| 同花顺 iFinD | MCP 平台/Token | 有官方 MCP 服务；未发现官方 GitHub Skill | 中高，商业授权 | 中高 | https://mcp.51ifind.com/ | iFinD MCP 平台提供 Auth Token；第三方/社区项目已封装 iFind MCP/Skill，但官方 GitHub Skill 未确认 |
| Bloomberg | Terminal/API | 未发现官方 Skill | 高，商业授权 | 中高 | https://github.com/msitt/blpapi-python | Bloomberg BLPAPI Python 包在 GitHub 可见，但使用依赖 Bloomberg 终端/服务器授权 |
| LSEG / Refinitiv | SDK/API | 未发现官方 Skill | 高，商业授权 | 中高 | https://github.com/LSEG-API-Samples/Example.DataLibrary.Python | LSEG Data Library / Workspace API 样例丰富，机构数据授权门槛高 |
| FactSet | SDK/API | 未发现官方 Skill | 高，商业授权 | 中高 | https://github.com/factset | FactSet 官方 GitHub 组织提供多语言 SDK，适合机构数据自动化 |
| Morningstar | API/Direct | 未发现官方 Skill | 中高，商业授权 | 中 | https://developer.morningstar.com | Morningstar 数据与 Direct 生态偏商业授权，公开 GitHub Skill 未发现 |
| S&P Global Market Intelligence / Capital IQ | API | 未发现官方 Skill | 中高，商业授权 | 中 | https://developer.spglobal.com | Capital IQ / S&P 数据接口偏企业订阅，自动化受授权约束 |
| Nasdaq Data Link | API/SDK | 未发现官方 Skill | 高 | 中高 | https://github.com/Nasdaq/data-link-python | 原 Quandl，Python 包公开，数据集按免费/付费授权分层 |
| Polygon.io / Massive | SDK/API | 未发现官方 Skill | 高 | 中高 | https://github.com/massive-com/client-python | 美股市场数据 REST/WebSocket API，官方 Python client |
| Alpaca | API/SDK/CLI 生态 | 未发现官方 Skill | 高 | 中高 | https://github.com/alpacahq/alpaca-py | 交易与行情 API 开放度高，适合 Agent 自动化但需风控 |
| Interactive Brokers | API/TWS Gateway | 未发现官方 Skill | 高，账户授权 | 中高 | https://github.com/InteractiveBrokers/tws-api-public | 交易与行情 API 成熟，依赖账户、TWS/IB Gateway |
| Tushare Pro | SDK/API | 未发现官方 Skill | 中高，积分/授权 | 中高 | https://github.com/waditu/tushare | A 股数据接口社区影响力强，非传统终端厂商 |
| AKShare | Python SDK | 社区 Skill 可用 | 中高，聚合公开源 | 中高 | https://github.com/akfamily/akshare | 开源财经数据接口库，覆盖 A 股、港美股、宏观等，适合 Agent 调用 |
| Baostock | Python SDK | 未发现官方 Skill | 中 | 中 | https://github.com/baostock/baostock | 免费证券数据接口，覆盖范围和稳定性低于商业终端 |
| 聚宽 JoinQuant | SDK/API | 未发现官方 Skill | 中高，平台授权 | 中 | https://www.joinquant.com | 量化研究与回测平台，数据接口主要在平台内使用 |
| 米筐 Ricequant | SDK/API | 未发现官方 Skill | 中高，平台授权 | 中 | https://www.ricequant.com | 量化投研平台，API/数据通常绑定平台环境 |

金融类小结：

- 国内机构级数据源里，Wind 已经有官方 `wind-skills`，iFinD 已有官方 MCP 平台；Choice 暂未发现官方 Agent Skill/MCP 公开入口。
- 海外机构级数据源如 Bloomberg、LSEG、FactSet、Morningstar、S&P 也类似，自动化能力强，但商业授权、合规和数据再分发限制重。
- 真正适合开源 Agent Skill 快速落地的是 AKShare、Tushare、Nasdaq Data Link、Polygon/Massive、Alpaca、IBKR 这类 SDK/API 可脚本化程度高的平台。
- 金融 Agent Skill 的风险点比办公类高：需要显式区分“数据查询/研究分析”和“下单/交易执行”，交易类必须加入权限、审计、确认与风控限制。

### 3.8 数字货币、比特币交易平台与链上基础设施

| 公司/平台 | 官方 CLI | 官方 Skill | 官方 MCP | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|---|
| Binance / 币安 | CLI/Skill hub 内工具 | 有 | 未确认官方 MCP | 高 | 高 | https://github.com/binance/binance-skills-hub | 官方 Binance Skills Hub，面向 AI agents 原生接入 crypto |
| BNB Chain | MCP 相关工具 | 有 | 有 MCP 指引 | 高 | 高 | https://github.com/bnb-chain/bnbchain-skills | 官方 BNB Chain Skills，指导安装和使用 BNB Chain MCP server |
| Coinbase | `awal` / AgentKit 工具链 | 有 | 有 | 高 | 高 | https://github.com/coinbase/agentic-wallet-skills | 官方 Agentic Wallet Skills；另有 AgentKit 与 Payments MCP |
| Coinbase Payments MCP | npx installer | 相关 | 有 | 高 | 高 | https://github.com/coinbase/payments-mcp | 钱包、onramp、x402 支付 MCP |
| Coinbase AgentKit | SDK/API | 相关 | 含 MCP 示例 | 高 | 高 | https://github.com/coinbase/agentkit | 为 AI agents 提供钱包和链上交互能力 |
| Base | SDK/MCP | 相关 | 有 | 高 | 高 | https://github.com/base/base-mcp-legacy | Base MCP legacy，连接 Base 网络和 Coinbase API |
| OKX | 有，`@okx_ai/okx-trade-cli` | 有 | 有 | 高 | 高 | https://github.com/okx/agent-skills | 官方 OKX Agent Skills；另有 agent-trade-kit MCP |
| OKX Agent Trade Kit | CLI/MCP | 相关 | 有 | 高 | 高 | https://github.com/okx/agent-trade-kit | OKX trading MCP server，连接 spot、swap、futures、options、grid bots |
| Kraken | 有，`kraken-cli` | CLI 内置 Agent 场景 | CLI 内置 MCP server | 高 | 高 | https://github.com/krakenfx/kraken-cli | 官方 AI-native CLI，覆盖 crypto、stocks、forex、derivatives |
| CoinMarketCap | API Skills | 有 | Skill 形式支持 MCP Skills | 高 | 高 | https://github.com/coinmarketcap-official/skills-for-ai-agents-by-CoinMarketCap | 官方 CoinMarketCap AI Agent Skills，覆盖 crypto、DEX、exchange、market API |
| Uniswap | SDK/API | 待复核 | 未确认官方 MCP | 高 | 中高 | 待补 | DEX 头部平台，官方 SDK/API 成熟但 Skill/MCP 官方源需继续确认 |
| MoonPay | SDK/API | 待复核 | 未确认官方 MCP | 高 | 中高 | 待补 | 法币出入金平台，Agent Skill 官方源需继续确认 |
| Bybit | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 高 | 中高 | 待补 | API/SDK 存在，官方 Agent Skill/MCP 未确认 |
| Bitget | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 高 | 中高 | 待补 | API/SDK 存在，官方 Agent Skill/MCP 未确认 |
| Gate.io | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 高 | 中高 | 待补 | API/SDK 存在，官方 Agent Skill/MCP 未确认 |
| KuCoin | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 高 | 中高 | 待补 | API/SDK 存在，官方 Agent Skill/MCP 未确认 |
| BitMEX | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 高 | 中高 | 待补 | 衍生品交易 API 成熟，Agent 入口未确认 |
| Deribit | API/SDK | 未确认官方 Skill | 未确认官方 MCP | 高 | 中高 | 待补 | 期权/衍生品交易 API 成熟，Agent 入口未确认 |
| DefiLlama | API/数据平台 | 未确认官方 Skill | 未确认官方 MCP | 高 | 高 | 待补 | DeFi 数据开放度高，Agent 入口多为社区 |
| CoinGecko | API/SDK | 未确认官方 Skill | MCP 线索待复核 | 高 | 高 | 待补 | 加密价格/市场数据平台，官方 MCP/Skill 源需确认 |

数字货币类小结：

- 官方 Agent 化最明确的是 Binance、Coinbase、OKX、Kraken、CoinMarketCap、BNB Chain。
- 交易平台类项目必须按权限分层：只读行情/账户查询、下单、转账、链上授权、私钥/钱包控制应分别审计。
- 对社区 MCP/Skill，尤其是可下单或转账的项目，应默认高风险，必须检查密钥存储、订单确认、额度限制、日志和撤销机制。

### 3.9 AI、模型平台与 Agent 基础设施

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| OpenAI | SDK/API | 有官方 Skill | 高 | 高 | https://github.com/openai/openai-python | 官方 Python SDK；Codex Skill 生态活跃 |
| Anthropic | SDK/API | 有官方 Skill | 高 | 高 | https://github.com/anthropics/anthropic-sdk-python | 官方 SDK 与 Claude Skills 生态 |
| Hugging Face | 有，hf CLI | 有官方 Skill | 高 | 高 | https://github.com/huggingface/huggingface_hub | Hub、Datasets、Spaces、模型训练与评测 |
| MiniMax | CLI/API | 有官方 Skill | 高 | 中高 | https://github.com/VoltAgent/awesome-agent-skills | MiniMax AI CLI 与 API 集成 |
| 阿里云百炼 Model Studio | 有 | 未发现官方 Skill | 高 | 中高 | https://github.com/modelstudioai/cli | Agent-first CLI，暴露模型、搜索、多模态和 workflow |
| 来也 ADP | 有 | 有 CLI + Skill | 中高 | 中高 | https://github.com/laiye-ai/adp-cli | 文档解析、分类、抽取、校验，面向人和 Agent |
| Pinecone | SDK/API | 有官方 Skill | 高 | 高 | https://github.com/pinecone-io/skills | 向量数据库官方 Agent Skills |
| Composio | API/平台 | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | 连接 1000+ 外部应用，托管认证 |
| Browserbase | CLI/API | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | 浏览器自动化平台，CLI + Skill |

### 3.10 设计、前端、移动与内容开发

| 公司/平台 | 官方 CLI | 官方 Skill | API/SDK 开放性 | 数据/接口开放性 | GitHub 地址 | 简短说明 |
|---|---|---|---|---|---|---|
| Figma | API/Plugin | 有官方 Skill | 中高 | 中高 | https://github.com/VoltAgent/awesome-agent-skills | 设计数据开放受权限与文件结构影响 |
| Angular | 有 Angular CLI | 有官方 Skill | 高 | 高 | https://github.com/angular/skills | Angular 官方 Skills，含新应用创建 |
| Flutter | 有 Flutter CLI | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | Flutter 官方 Skill 覆盖开发与升级 |
| Expo | 有 EAS/Expo CLI | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | React Native/Expo 构建、部署、升级 |
| Cypress | 有 | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | E2E 测试工作流 |
| WordPress | 有 WP-CLI | 有官方 Skill | 高 | 高 | https://github.com/VoltAgent/awesome-agent-skills | CMS 运维、内容管理、自动化 |

## 4. 中国厂商开放性观察

| 方向 | 领先项目 | 开放性判断 | 说明 |
|---|---|---|---|
| 协作办公 | 飞书、钉钉 | 高 | 官方 CLI 明确面向 AI Agent，业务对象 API 化程度高 |
| 文档知识库 | 金山文档、语雀 | 中高 | 已有 Skill/MCP/Plugin，但部分能力仍需账号与权限 |
| 办公套件 | Kdocs/WPS、飞书、钉钉、Google Workspace、Microsoft 365 | 高到中高 | 办公对象结构化程度高，是 Agent Skill 最容易产品化的方向之一 |
| 云平台 | 阿里云、腾讯云、火山引擎、华为云 | 高到中高 | 官方 CLI/OpenAPI 成熟；华为云已有官方 Agent Skills |
| 模型平台 | MiniMax、阿里云百炼 | 中高 | API 开放较强，Agent-first CLI 开始出现 |
| 金融数据 | Wind、Choice、iFinD、Tushare、AKShare | 高到中 | Wind 官方 Skill 已出现；iFinD 有官方 MCP 平台；Choice 仍偏传统终端/API；开源数据 SDK 更适合快速 Skill 化 |
| 数字货币交易 | Binance、Coinbase、OKX、Kraken、CoinMarketCap | 高到中 | 官方 Skill/MCP/CLI 已快速出现，但交易和转账风险显著高于只读数据接口 |
| 数据供应商 | 小红书、微信、公众号、微信读书 | 低到中 | 平台数据开放限制明显，社区项目先行 |
| 数据库/数仓 | 暂未发现头部中国厂商官方 Skill | 中 | CLI/SDK 可能存在，但 Agent Skill 生态尚不突出 |

## 5. 优先跟踪清单

| 优先级 | 厂商/项目 | 为什么值得跟踪 |
|---|---|---|
| P0 | 飞书 `larksuite/cli` | 中国官方 Agent CLI/Skill 最完整样本 |
| P0 | 钉钉 Workspace CLI | 国内企业协作平台的官方 Agent 化入口 |
| P0 | GitHub `cli/cli` | 官方 CLI 已内置 Skill 分发与安装能力 |
| P0 | 华为云 Agent Skills | 中国云厂商直接发布官方 Skills 的重要信号 |
| P1 | 金山文档 WPS AirPage Skill | 文档编辑高度适合 Agent 自动化 |
| P1 | 语雀 Ecosystem | MCP + Skills + Plugin 组合，知识库场景清晰 |
| P1 | Wind / Choice / iFinD | Wind 已有官方 Skill，iFinD 有官方 MCP 平台，Choice 尚未发现官方 Skill/MCP；适合继续跟踪金融数据 Agent 化 |
| P1 | AKShare / Tushare | 开源财经数据接口更容易直接 Skill 化 |
| P1 | 阿里云百炼 Model Studio CLI | 国内模型平台 Agent-first CLI 代表 |
| P1 | Pinecone Skills | 数据基础设施厂商发布官方 Skills 的代表 |
| P2 | 小红书 / 微信公众号社区 Skill | 平台官方缺位但市场需求强 |
| P2 | Zotero CLI 社区项目 | 文献管理官方 Skill 缺口明显 |

## 6. 下一步建议

1. 登录 GitHub CLI：`gh auth login`，之后可直接用 `gh search repos --json ...` 扩展到 200+ 仓库。
2. 对每个行业头部厂商建立定期扫描：关键词包括 `official cli`、`agent skills`、`SKILL.md`、`MCP server`、`OpenAPI`。
3. 为中国厂商单独维护“开放性雷达”：协作办公、云平台、模型平台、内容平台、数据供应商。
4. 对未发现官方 Skill 但 API 开放度高的厂商，标记为“可自建 Skill 高潜力”。
