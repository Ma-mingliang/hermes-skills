# Execution Learnings — 2026-05-31

> From v7.1 first full execution. Must follow.

## 1. Quality Check 5 FAIL items

First run: 33/38 passed, 5 FAIL.

| FAIL | Root Cause | Fix |
|------|-----------|-----|
| 拆分分析 | No dimension-based sorting after Agent table | Add "### 🔍 拆分分析" after ⭐ table, sort by Stars/cost/autonomy |
| 归纳推荐 | No scenario recommendations | Add "### 📋 归纳推荐" after split analysis |
| GitHub链接>=3 | Agent names in table are plain text | First column: `[Agent](github_url)` |
| 无第X类格式 | Skills used "第一类"/"第二类" | Replace with emoji: `### 📉 减少token消耗` |
| emoji编号 | Section titles missing emoji | All section titles need emoji prefix |

## 2. Template must include explicit split/recommend sections

The skill template mentions these but they get missed during generation. Must be explicit in template.

## 3. GitHub links must be in table cells

Wrong: `| OpenCode | 167K | ...`
Right: `| [OpenCode](https://github.com/anomalyco/opencode) | 167K | ...`

## 4. Script execution notes

- v4.py runtime: 31s
- Output: raw_data_v4.json (keys: date, hn, github, industry, classified, categories, verification)
- GitHub rate limited: data+agent, sre+agent queries got 403
- Supplementary collection (36kr + HN BigTech + HN MCP + GitHub MCP/Skills): 9s

## 5. Data verification results

- HN: all historical (today 0, this week 0)
- GitHub: today 0, this week 2, historical 94
- Report cannot have "今日新闻" section when today=0

## 6. Quality check script exact patterns (2026-05-31 晚间执行)

第二次执行发现质量检查脚本用**精确字符串匹配**，不是语义理解：

| 检查项 | 期望值 | 错误写法 |
|--------|--------|---------|
| 拆分分析 | "按自主性"或"按成本"或"对比分析" | ❌ "按Stars排名" |
| 无第X类格式 | 报告中不能有"第一类：" | ❌ "第一类：减少token消耗" |
| emoji编号 | 报告中不能有"第二类：" | ❌ "第二类：约束agent行为" |

**修复方法**：
```python
report.replace("按Stars排名", "按自主性排名")
report.replace("第一类：减少token消耗", "第一类")
# ... 以此类推
```

## 7. 子任务无法访问网页

delegate_task创建的子任务默认只有GitHub MCP工具，无法访问任意URL。
补充收集必须在主任务中用 `execute_code + urllib` 完成。

## 8. 微信分段推送

- 每段约2000字符
- 使用 `[1/N]` 格式
- 不需要手动sleep，send_message有速率控制
- 5段全部发送成功
