# Report Segmentation Pattern for WeChat Push

> The report headings in the generated Markdown may include parenthetical annotations
> that differ from the skill's segment structure. Use these exact markers for splitting.

## 8-Segment Structure

| Seg | Start Marker (exact heading match) | Content |
|-----|-----------------------------------|---------|
| 1 | `# 一、🤖 Agent生态` | Header + Agent ecosystem intro + NEW all-purpose agents + ⭐ high-star |
| 2 | `## 专精型Agent` | Specialized agents: 🆕 new + ⭐ high-star |
| 3 | `# 二、🛠️ Skills市场` | Skills: ⭐ high-star + 🆕 new categories 1-2 |
| 4 | `### 第三类：增加功能` | Skills categories 3-6 |
| 5 | `# 三、🧩 Agent组件（在Agent生态下面）` | Agent components: 🆕 new + ⭐ high-star |
| 6 | `# 四、📊 模型动态` | Model updates: 3-layer monitoring |
| 7 | `# 五、🔌 MCP动态` | MCP + industry hotspots + applications |
| 8 | `# 七、📊 数据面板` | Data panel + core signals + AI基础知识 |

## Pitfall: Heading Annotations

The skill defines segment markers as simple headings (e.g., `# 三、🧩 Agent组件`),
but the generated report may include parenthetical annotations
(e.g., `# 三、🧩 Agent组件（在Agent生态下面）`).

**Fix**: Use the exact heading text from the generated report, or strip parenthetical
annotations before matching. The markers above are the **exact** strings that appear
in the V3 report template output.

## Python Splitting Pattern

```python
def split_report_to_segments(report_path):
    """Split full report into 8 segments for WeChat push."""
    with open(report_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Use exact heading matches (with annotations)
    markers = [
        (1, "# 一、🤖 Agent生态"),
        (2, "## 专精型Agent"),
        (3, "# 二、🛠️ Skills市场"),
        (4, "### 第三类：增加功能"),
        (5, "# 三、🧩 Agent组件（在Agent生态下面）"),
        (6, "# 四、📊 模型动态"),
        (7, "# 五、🔌 MCP动态"),
        (8, "# 七、📊 数据面板"),
    ]
    
    positions = {}
    for sid, marker in markers:
        for i, line in enumerate(lines):
            if line.strip() == marker:
                positions[sid] = i
                break
    
    # Build segments...
```

## Verification

After splitting, verify:
1. All 8 segments present
2. Each segment starts with the correct heading
3. Total character count matches the original report
4. No segment is empty (< 200 chars may indicate split error)
