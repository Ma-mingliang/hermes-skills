# Agent报告生成执行清单

## 📋 执行前确认
- [ ] 分类已完成
- [ ] 已获取classification_log.json
- [ ] 已确认Agent列表

### 0. 报告去重验证（必须执行，最高优先级）
**目标**：确保报告中没有重复项目出现在不同板块

**验证流程**：
```python
def check_report_duplicates(report_content):
    """检查报告中是否有重复项目"""
    projects_in_sections = {}
    
    # 提取每个板块的项目
    sections = report_content.split('# ')
    for section in sections:
        section_name = section.split('\n')[0].strip()[:50]
        # 提取项目名称（简化版）
        project_names = extract_project_names(section)
        
        for name in project_names:
            if name not in projects_in_sections:
                projects_in_sections[name] = []
            projects_in_sections[name].append(section_name)
    
    # 检查重复
    duplicates = {name: sections for name, sections in projects_in_sections.items() if len(sections) > 1}
    return duplicates

# 生成报告后执行检查
duplicates = check_report_duplicates(report_content)
if duplicates:
    print("⚠️ 发现重复项目：")
    for name, sections in duplicates.items():
        print(f"  {name} 出现在：{', '.join(sections)}")
    # 处理重复项目
    for name, sections in duplicates.items():
        # 保留第一次出现的板块，删除后续重复
        remove_duplicates_from_report(name, sections[1:])
else:
    print("✅ 报告中无重复项目")
```

**验证清单**：
- [ ] 生成报告后是否执行重复检查
- [ ] 发现重复项目是否处理
- [ ] 是否保留第一次出现的板块
- [ ] 是否删除后续重复

**输出**：
```
报告去重验证结果：
- 检查项目数：X
- 重复项目：Y个（已处理）
- 无重复：✅
```


## 🔍 Agent报告生成清单

### 1. Agent速览表（必须）
**目标**：生成全能Agent速览表

**必须包含的Agent**：
- [ ] Claude Code
- [ ] OpenAI Codex
- [ ] Cursor
- [ ] OpenClaw
- [ ] Hermes Agent
- [ ] Langflow
- [ ] Dify

**表格列（P20/P21/P22规则）**：
| Agent | 解决什么痛点 | 核心优势（对比同类） | 定价 | 性价比 |

**验证清单**：
- [ ] 每个Agent是否包含"解决什么痛点"列
- [ ] 每个Agent的核心优势是否对比同类Agent
- [ ] 是否包含OpenClaw
- [ ] Hermes的核心优势是否是"自适应进化"（对比OpenClaw）

**输出**：
```
Agent速览表：
- 包含Agent数：X
- 痛点列：✅
- 核心优势对比：✅
- 包含OpenClaw：✅
```

### 2. 新出现Agent（必须）
**目标**：详细介绍今日新出现的Agent

**每个Agent必须包含**：
- [ ] 名称
- [ ] Stars数
- [ ] 解决什么痛点
- [ ] 核心功能
- [ ] 技术原理
- [ ] GitHub链接
- [ ] 前辈对比（必须！）

**前辈对比格式**：
```
👨‍💼 前辈对比：vs XXX
| 维度 | XXX | 本Agent |
|------|-----|---------|
| 定位 | ... | ... |
| 功能 | ... | ... |
| 复杂度 | ... | ... |

💡 本Agent解决XXX的问题：
1. 问题1 → 解决方案1
2. 问题2 → 解决方案2
```

**验证清单**：
- [ ] 每个Agent是否包含所有必填项
- [ ] 前辈对比是否完整（表格+解决的问题）
- [ ] 痛点描述是否通俗易懂
- [ ] 技术原理是否清晰

**输出**：
```
新出现Agent：
- 数量：X
- 必填项完整：Y/X
- 前辈对比完整：Z/X
```

### 3. 高星Agent（必须）
**目标**：介绍今日高星Agent

**必须包含**：
- [ ] 名称
- [ ] Stars数
- [ ] 解决什么痛点
- [ ] 核心功能
- [ ] GitHub链接

**验证清单**：
- [ ] 每个Agent是否包含所有必填项
- [ ] 是否与速览表重复（如果不重复，则添加）

**输出**：
```
高星Agent：
- 数量：X
- 必填项完整：Y/X
```

### 4. 专精Agent（必须）
**目标**：介绍今日专精Agent

**如果当日没有新的专精Agent**：
- 推荐5个高星的专精Agent（含详细描述+前辈对比）

**验证清单**：
- [ ] 是否有新的专精Agent
- [ ] 如果没有，是否推荐了5个高星专精Agent
- [ ] 每个专精Agent是否包含所有必填项

**输出**：
```
专精Agent：
- 新增数量：X
- 推荐数量：Y
- 必填项完整：Z
```

### 5. Agent组件（必须）
**目标**：介绍Agent组件

**必须包含**：
- [ ] 名称
- [ ] 解决什么问题（原始Agent的什么不足）
- [ ] 核心原理
- [ ] 适用Agent
- [ ] GitHub链接
- [ ] Stars数

**验证清单**：
- [ ] 每个组件是否包含所有必填项
- [ ] 是否说明了解决哪些Agent的什么问题
- [ ] 是否在Agent生态下面（不是独立板块）

**输出**：
```
Agent组件：
- 数量：X
- 必填项完整：Y/X
- 在Agent生态下：✅
```

## ✅ 执行确认

**Agent报告生成完成后，必须输出以下确认信息**：
```
📊 Agent报告生成完成确认
====================
1. 速览表：X个Agent，含痛点列✅，含OpenClaw✅
2. 新出现Agent：X个，必填项完整Y/X，前辈对比完整Z/X
3. 高星Agent：X个，必填项完整Y/X
4. 专精Agent：新增X个，推荐Y个
5. 组件：X个，必填项完整Y/X

总计：Agent报告生成完成，共X个Agent，Y个组件
```

## ⚠️ 异常处理

**如果某个Agent信息不完整**：
1. 标记为"待补充"
2. 尝试从其他来源获取
3. 如果无法获取，跳过该Agent

**如果前辈对比找不到**：
1. 搜索GitHub上功能相似的项目
2. 搜索已知的高星项目
3. 如果仍找不到，标记为"前辈对比待补充"

## 📝 执行记录

**必须保存到**：`D:/openclaw-hermes/data/daily/YYYY-MM-DD/agent_report_log.json`

**记录内容**：
```json
{
  "date": "2026-05-30",
  "overview_table": {"agents": 7, "has_pain_point": true, "has_openclaw": true},
  "new_agents": {"count": 3, "complete": 3, "predecessor_comparison": 3},
  "high_star_agents": {"count": 5, "complete": 5},
  "specialized_agents": {"new": 0, "recommended": 5},
  "components": {"count": 2, "complete": 2}
}
```
