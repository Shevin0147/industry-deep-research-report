# Industry Deep Research Report

[![Validate](https://github.com/wyh583/industry-deep-research-report/actions/workflows/validate.yml/badge.svg)](https://github.com/wyh583/industry-deep-research-report/actions/workflows/validate.yml)
[![GitHub release](https://img.shields.io/github/v/release/wyh583/industry-deep-research-report)](https://github.com/wyh583/industry-deep-research-report/releases)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

[English](./README.md) · **简体中文**

一个面向行业研究、市场进入、产品立项、商业投入与投资判断的 Codex Skill。

它将公开资料转化为带证据边界、竞争性假设、市场模型和质量门禁的中文决策报告，而不只是汇总搜索结果。

## 核心能力

- 固定的 10 章决策型报告结构
- `quick`、`standard`、`deep` 三种研究深度
- 竞争性假设、反证搜索与置信度记录
- 结论—证据映射及来源独立性检查
- 自上而下与自下而上的市场规模测算
- 单位经济、盈亏平衡与敏感性分析
- L1—L4 决策证据等级
- 通用证据内核与条件化行业证据包
- 自动质量门禁及结构化 `.research/` 档案
- HTML、PDF 与 HTMLSlides 输出流程

## 行业证据包

首版包含：

- `consumer-retail`
- `saas-ai`
- `manufacturing`
- `ecommerce-platform`
- `healthcare`
- `restaurant-local-service`

每次研究加载一个主行业包，并可选择一个次行业包。无法可靠分类时回退到通用证据内核。

## 仓库结构

```text
.
├── README.md
├── .gitignore
└── industry-deep-research-report/
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

## 安装

将仓库中的 `industry-deep-research-report` 子目录复制到 Codex skills 目录。

Windows 示例：

```powershell
$codexSkills = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME "skills"
} else {
  Join-Path $env:USERPROFILE ".codex\skills"
}

Copy-Item `
  -LiteralPath ".\industry-deep-research-report" `
  -Destination (Join-Path $codexSkills "industry-deep-research-report") `
  -Recurse `
  -Force
```

如果你的 Codex skills 目录不同，请替换目标路径。

## 使用

在 Codex 中调用 Skill，并给出行业、地区、时间范围和决策目标，例如：

```text
使用 $industry-deep-research-report，
分析美国宠物智能用品市场，判断是否值得启动低成本 MVP。
```

研究深度与决策等级相互独立：

| 等级 | 支持的决策 |
|---|---|
| L1 | 是否继续研究 |
| L2 | 是否启动低成本 MVP 或验证 |
| L3 | 是否组建团队并进行商业投入 |
| L4 | 是否进行投资、并购或规模扩张 |

## 报告校验

```powershell
python .\industry-deep-research-report\scripts\validate_report.py `
  --report <report.md> `
  --research-dir <.research目录> `
  --mode standard
```

- 没有阻断项时退出码为 `0`。
- 存在阻断项时退出码为 `1`。
- 详细结果会写入 `.research/validation.json`。

## 运行要求

- Python 3.9 或更高版本
- 校验脚本仅使用 Python 标准库
- PDF 导出需要本机可用的 Chrome 或 Edge
- HTMLSlides 输出需要相应的 HTML Slides Skill

## 数据与安全

仓库不应包含：

- API Key、访问令牌或密码
- 真实研究项目的 `.research/` 档案
- 未脱敏的用户资料
- 生成的报告、PDF、PPT 或 HTML 文件

## License

本仓库当前未附加开源许可证。公开访问不代表授予复制、修改或再分发权利；如需开源使用，请在后续版本明确选择许可证。
