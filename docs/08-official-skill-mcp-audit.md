# 官方 Skill / MCP 服务复核表

更新日期：2026-07-06

## 复核结论

上一版把 Wind 标为“未发现官方 Skill”不准确。复核后确认：

- Wind / 万得：已有官方 `wind-skills` 仓库，包含 `wind-mcp-skill`、`wind-find-finance-skill`、`wind-alice` 等。
- 同花顺 iFinD：有官方 MCP 平台 `https://mcp.51ifind.com/`，需要 Auth Token；未确认官方 GitHub Skill 仓库。
- 东方财富 Choice：确认有 Choice 终端、数据库、量化接口等产品，但未发现官方 Agent Skill/MCP 公开入口。

## 金融数据与终端

| 厂商/平台 | 官方 Skill | 官方 MCP | 地址 | 复核状态 | 说明 |
|---|---|---|---|---|---|
| Wind / 万得 | 有 | 有，`wind-mcp-skill` | https://github.com/Wind-Information-Co-Ltd/wind-skills | 已确认 | 官方 monorepo，收录 Wind 自家数据与金融分析 Skill；安装命令支持 `npx skills add Wind-Information-Co-Ltd/wind-skills --skill wind-mcp-skill -g -y` |
| Wind AIFinMarket | 相关 | 相关 | https://aifinmarket.wind.com.cn/#/home | 已确认 | Wind API Key / 开发者入口，`wind-mcp-skill`、`wind-alice` 需要 Key |
| 同花顺 iFinD | 未确认官方 GitHub Skill | 有官方 MCP 平台 | https://mcp.51ifind.com/ | 部分确认 | MCP 平台提供 Auth Token；社区/第三方项目已封装 iFind MCP/Skill |
| 东方财富 Choice | 未发现 | 未发现 | https://choice.eastmoney.com | 未发现官方 Skill/MCP | 官网确认 Choice 智能金融终端、Choice 数据库、Choice 量化接口等产品 |
| Tushare Pro | Wind 仓库中有 `tushare-finance-skill` | 未确认官方 MCP | https://github.com/Wind-Information-Co-Ltd/wind-skills | Skill 已确认，官方归属需区分 | Wind 官方仓库收录 Tushare 数据 Skill，但 Tushare 本身不是 Wind |
| AKShare | 社区/本地 Skill 可用 | 社区 MCP 可用 | https://github.com/akfamily/akshare | 非官方 Agent Skill | 开源数据接口库，适合自建 Skill/MCP |
| Bloomberg | 未发现官方 Skill | 未发现官方 MCP | https://github.com/msitt/blpapi-python | 未发现官方 Skill/MCP | 有 Bloomberg Python API；MCP 多为社区实现 |
| LSEG / Refinitiv | 未发现官方 Skill | 未发现官方 MCP | https://github.com/LSEG-API-Samples/Example.DataLibrary.Python | 未发现官方 Skill/MCP | 官方 SDK/API 样例丰富，MCP/Skill 未确认 |
| FactSet | 未发现官方 Skill | 未发现官方 MCP | https://github.com/factset | 未发现官方 Skill/MCP | 官方 SDK 组织存在，未确认 Agent Skill/MCP |

## 办公、协作与知识库

| 厂商/平台 | 官方 Skill | 官方 MCP | 地址 | 复核状态 | 说明 |
|---|---|---|---|---|---|
| Kdocs / WPS 365 AirPage | 有 | 通过本地 CLI，不是典型 MCP | https://github.com/WPS-SmartDocs/WPS-AirPage-Skill | 已确认 | 官方 WPS AirPage CLI Skill，支持 kdocs / 365.kdocs.cn 文档创建、编辑、表格、图片、评论 |
| 飞书 / Lark / Feishu | 有，CLI 自带 20+ Agent Skills | CLI/命令网关形态 | https://github.com/larksuite/cli | 已确认 | 官方 Lark/Feishu CLI，200+ commands，面向 humans and AI Agents |
| 钉钉 / DingTalk | 有，Workspace CLI 面向 Agent | 基于 DingTalk MCP metadata 的 CLI | https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli | 已确认 | 官方开源跨平台 CLI，面向人类用户和 AI Agent |
| 语雀 / Yuque | 有 | 有，yuque-mcp | https://github.com/yuque/yuque-ecosystem | 已确认 | 语雀 AI Ecosystem，包含 MCP Server、Skills、Plugin |
| 语雀 Plugin | 有 | 打包 MCP + Skills | https://github.com/yuque/yuque-plugin | 已确认 | Claude Code Plugin，一键集成语雀 AI 能力 |
| Notion | 未按 Skill 形态确认 | 有官方 MCP Server | https://github.com/makenotion/notion-mcp-server | 已确认 MCP | 官方 Notion MCP Server，可读写 Notion workspace |
| Slack | Plugin 形态 | 有官方 hosted MCP server | https://github.com/slackapi/slack-mcp-plugin | 已确认 MCP/Plugin | 官方 Slack MCP Plugin 连接 Slack hosted MCP server |
| GitHub | 有，`cli/cli` 中 `gh` Skill | 有官方 MCP Server | https://github.com/cli/cli / https://github.com/github/github-mcp-server | 已确认 | GitHub CLI Skill 已本机安装；GitHub MCP Server 官方开源 |

## 需要继续跟踪

| 厂商/平台 | 原因 |
|---|---|
| 东方财富 Choice | 金融终端与量化接口很重要，但未发现官方 Skill/MCP 入口 |
| 同花顺 iFinD | 官方 MCP 平台已确认，但官方 GitHub Skill 仓库未确认 |
| Bloomberg / LSEG / FactSet / Morningstar | 官方 API/SDK 成熟，但 Agent Skill/MCP 多数仍是社区实现或未公开 |
| 国内数据库/数仓厂商 | 暂未看到类似 Wind、飞书、钉钉这种官方 Agent Skill/MCP 形态 |

