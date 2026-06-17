# AI 日报同步到 Obsidian

## 源目录结构（关键）

**源路径**: `D:/openclaw-hermes/data/daily/`

目录结构是**日期子目录**，不是扁平 .md 文件：
```
daily/
├── 2026-05-27/
│   ├── report.md          ← 主日报文件（必须存在）
│   ├── cross_ref.json     ← 辅助数据
│   ├── raw_search.json
│   └── ...
├── 2026-05-28/
│   ├── report.md
│   └── ...
├── 2026-06-01/            ← 空目录（无日报）
├── 2026-06-06/
│   ├── day1_content.md    ← ⚠️ 非日报内容（AI教育课程）
│   ├── day1_story.md
│   └── ...
```

### 发现最新日报的逻辑（必须按此顺序）

1. 列出 `D:/openclaw-hermes/data/daily/` 下所有子目录
2. **倒序排列**（最新日期在前）
3. 逐个检查是否存在 `report.md` — **只有含 report.md 的才是日报**
4. ⚠️ 并非所有日期目录都是日报！有些包含教育课程内容（如 `day1_content.md`、`day1_story.md`）
5. 有些目录可能为空（0 items）

### ⚠️ 无 report.md 时的处理（2026-06-06 实际案例）

2026-06-06 目录不含 `report.md`，只有：
- `day1_content.md` / `day1_story.md`（AI基础教育 Day 1）
- `day2_content.md` / `day2_story.md`（AI基础教育 Day 2）

**正确行为**：跳过，不作为日报同步。这些是教育课程内容，不是日报。

**错误行为**（2026-06-06 实际发生）：将 4 个文件合并为一个 `2026-06-06.md` 写入 Vault。
教训：**严格按 report.md 判断**，不要因为有 .md 文件就认为是日报。目录中有其他 .md 文件不代表它是日报。

### 决策树：遇到无 report.md 的目录

```
目录有 report.md?  → YES → 读前100字验证含"日报" → YES → 同步
                                                  → NO  → 跳过（非新闻日报内容）
                   → NO  → 跳过（不是日报）
                             即使有其他 .md 文件也跳过
                             这些可能是课程/教育/辅助内容
```

### ⚠️ 常见陷阱

| 陷阱 | 说明 |
|------|------|
| 假设源是扁平 .md 文件 | 实际是 `YYYY-MM-DD/report.md` 子目录结构 |
| **用 glob("*.md") 扫描 daily 根目录** | **返回 0 结果！根目录下无 .md 文件，全是日期子目录。必须先 `os.listdir()` 拿子目录列表，再逐个检查子目录里的 report.md** |
| 把所有日期目录当日报 | 需检查 `report.md` 是否存在 |
| **凭 report.md 存在就认定是日报** | **需验证内容：读前 100 字检查是否含"日报"关键词。2026-06-06 的文件不含"日报"，是教育课程** |
| 忽略空目录 | `2026-06-01` 等目录可能为空 |
| 用 terminal 在 Windows 上 ls | WSL relay 可能失败，用 `execute_code + os` 模块 |
| 不检查 Obsidian 已有版本 | 可能已同步过，需对比 |
| **frontmatter 格式凭记忆写** | **必须先读 Vault 中已有文件确认实际格式** |

### frontmatter 格式校准（必须做）

⚠️ **不要凭记忆或参考文件中的模板写 frontmatter！**
实际 Vault 中已有文件的格式才是 source of truth。

已确认的实际格式（读取 `D:/ObsidianVault/daily/2026-05-31.md` 得到）：
```yaml
---
date: 2026-05-31
type: ai-daily-digest
tags:
  - ai
  - daily
  - news
ai-first: true
```

与参考文件中的模板差异：
- 参考模板 tags: `[ai-news, daily-digest, ai-first]`
- 实际 Vault tags: `[ai, daily, news]`（更简洁）

**规则**：每次同步前，先 `read_file` 一个已有 Vault 文件，确认 frontmatter schema。
如果参考模板与实际不符，以实际为准，并更新参考模板。

## 同步规则

### 目标路径
`D:/ObsidianVault/daily/YYYY-MM-DD.md`

### 文件格式（添加 frontmatter + 前言后写入）

⚠️ **先读一个已有 Vault 文件确认实际 frontmatter 格式，再写！**

以下为已确认的实际格式（来源：2026-05-31.md）：
```yaml
---
date: YYYY-MM-DD
type: ai-daily-digest
tags:
  - ai
  - daily
  - news
ai-first: true
---

# AI 日报 | YYYY-MM-DD

## For future Claude
这是 YYYY-MM-DD 的 AI 日报，包含 [简述主要内容]。

---

[report.md 原始内容]
```

### 自动同步
- Cron Job: 每天 09:00
- 检查新日报 → 添加 frontmatter → 复制到 Vault

### 推荐实现（execute_code + Python）

```python
import os

daily_dir = r"D:\openclaw-hermes\data\daily"
obsidian_dir = r"D:\ObsidianVault\daily"

# 1. 找到含 report.md 的最新日期目录（⚠️ 不能用 glob，根目录无 .md 文件）
report_dates = []
for d in sorted(os.listdir(daily_dir), reverse=True):
    report_path = os.path.join(daily_dir, d, "report.md")
    if os.path.isfile(report_path):
        # 2. 验证是日报而非其他内容
        with open(report_path, 'r', encoding='utf-8') as f:
            head = f.read(100)
        if '日报' in head:
            report_dates.append(d)

if not report_dates:
    print("📭 无新日报")
else:
    latest = report_dates[0]
    dest = os.path.join(obsidian_dir, f"{latest}.md")

    if os.path.exists(dest):
        print(f"⏭️ {latest}.md 已存在")
    else:
        with open(os.path.join(daily_dir, latest, "report.md"), 'r', encoding='utf-8') as f:
            content = f.read()

        # ⚠️ 校准 frontmatter：先读已有文件确认格式
        existing_files = [f for f in os.listdir(obsidian_dir) if f.endswith('.md') and not f.startswith('.')]
        # (此处假设已确认格式如下)

        frontmatter = f"""---
date: {latest}
type: ai-daily-digest
tags:
  - ai
  - daily
  - news
ai-first: true
---

# AI 日报 | {latest}

## For future Claude
这是 {latest} 的 AI 日报，包含最新 AI 新闻与发展动态。

---

"""
        os.makedirs(obsidian_dir, exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)
        print(f"✓ 已同步 {latest}.md")
```

## AI 课程同步

### 目标路径
`D:/ObsidianVault/Learning/AI通史与基础知识.md`

### 内容
- 课程概览（60天，10周）
- 两条主线框架
- 热词清单
- 进度追踪
