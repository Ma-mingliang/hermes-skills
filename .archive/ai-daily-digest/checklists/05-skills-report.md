# Skills报告生成执行清单

## 📋 执行前确认
- [ ] 分类已完成
- [ ] 已获取classification_log.json
- [ ] 已确认Skills列表

### 详细检查要求（必须逐项核对）

#### Skills板块检查
1. **每个Skill必须包含**：
   - [ ] 名称+Stars+GitHub链接
   - [ ] 痛点类型标注（9种类型之一）
   - [ ] 详细原理分析（🎯原理+🔧操作+📊效果+👤案例）
   - [ ] 前辈对比表（功能/成本/自主性/易用性/适用场景）
   - [ ] 真实使用案例

2. **检查方法**：
```python
def check_skill_completeness(skill):
    required_fields = ["name", "stars", "github_link", "pain_point", "principle", "predecessor_comparison", "real_case"]
    for field in required_fields:
        if field not in skill or not skill[field]:
            print(f"⚠️ Skill {skill['name']} 缺少 {field}")
            return False
    return True
```

#### MCP板块检查
1. **每个MCP项目必须包含**：
   - [ ] 名称+Stars+GitHub链接
   - [ ] 功能描述
   - [ ] 适用场景
   - [ ] 与Agent/Skills的关联

2. **检查方法**：
```python
def check_mcp_completeness(mcp):
    required_fields = ["name", "stars", "github_link", "function", "scenario", "agent_relation"]
    for field in required_fields:
        if field not in mcp or not mcp[field]:
            print(f"⚠️ MCP {mcp['name']} 缺少 {field}")
            return False
    return True
```

#### 模型动态检查
1. **必须包含**：
   - [ ] 模型版本精确到小版本
   - [ ] 综合能力排名
   - [ ] 编码能力排名
   - [ ] 性价比排名
   - [ ] 热点模型事件

2. **检查方法**：
```python
def check_model_dynamics(model_data):
    required_fields = ["version", "comprehensive_ranking", "coding_ranking", "cost_ranking", "hot_events"]
    for field in required_fields:
        if field not in model_data or not model_data[field]:
            print(f"⚠️ 模型动态缺少 {field}")
            return False
    return True
```

#### 格式检查
1. **板块顺序**：
   - [ ] Agent生态 → Skills市场 → 模型动态 → 行业应用 → MCP动态 → 数据面板 → 核心信号
   - [ ] 无板块标题重复

2. **链接检查**：
   - [ ] 所有事件有可点击的原文链接
   - [ ] 链接格式正确（不是"36氪"两个字，而是完整URL）


## 🔍 Skills报告生成清单

### 1. Skills内容详略规则（P18规则）
**目标**：所有Skills不论Stars高低，格式统一

**完整格式（必须）**：
```
**名称** ⭐Stars — 简短描述
🔗 GitHub链接

🎯 痛点：解决什么问题
📊 原理：技术原理
💡 案例：使用案例
📈 效果：量化效果

👨‍💼 前辈对比：vs XXX
| 维度 | XXX | 本Skill |
|------|-----|---------|
| ... | ... | ... |

💡 本Skill解决XXX的问题：
1. 问题1 → 解决方案1
```

**验证清单**：
- [ ] 每个Skills是否按完整格式写
- [ ] 不论Stars高低，格式是否统一
- [ ] Stars<50的Skills是否至少包含：名称+痛点+原理+GitHub链接

**输出**：
```
Skills内容详略验证：
- 总Skills数：X
- 完整格式：Y/X
- 简写格式（Stars<50）：Z/X
```

### 2. Skills分类（必须）
**目标**：将Skills分为6类

**6类Skills**：
1. **减少token消耗**：压缩输入、精简上下文、智能路由（context-compression、planning-before-execution、token-saver、context-budget、prompt-optimizer）
2. **约束行为**：限制Agent行为范围、安全防护、流程规范（safety-guard、security-review、process-thinking、reasoning-trace）
3. **增加功能**：扩展Agent能力、添加新工具/新能力（content-search-organizer、url-summary、duckduckgo-search、instructor、scrapling）
4. **科研辅助**：论文阅读、文献检索、实验设计、学术写作（ARIS系列、deep-research、research-lit、research-ops）
5. **检测正常工作**：验证/监控/审计类skill，确保Agent输出质量和系统运行正常。包括质量验证（verification-loop）、skill库存盘点（skill-stocktake）、服务可用性监控（canary-watch）、缓存效率审计（cache-audit）、上下文消耗审计（context-budget）、工具成本审计（ecc-tools-cost-audit）、工作区安全审计（workspace-surface-audit）、安全扫描（security-scan）
6. **补充类/其他**：独立于前5类之外的skills、资源/索引/元信息集合、配置文档类skill（awesome-claude-skills、awesome-hermes-agent、hermes-atlas、skill-scout、hermes-agent）

**验证清单**：
- [ ] 每个Skills是否归入正确的类别
- [ ] 每个类别是否有足够的Skills（至少1个）
- [ ] 是否有遗漏的类别

**输出**：
```
Skills分类结果：
- 第一类（减少token）：X个
- 第二类（约束行为）：Y个
- 第三类（增加功能）：Z个
- 第四类（科研辅助）：W个
- 第五类（检测正常）：V个
- 第六类（补充类）：U个
```

### 3. 前辈对比（必须）
**目标**：每个Skills必须有前辈对比

**前辈对比格式**：
```
👨‍💼 前辈对比：vs XXX
| 维度 | XXX | 本Skill |
|------|-----|---------|
| 策略 | ... | ... |
| 原理 | ... | ... |
| 适用场景 | ... | ... |
| 效果 | ... | ... |

💡 本Skill解决XXX的问题：
1. 问题1 → 解决方案1
2. 问题2 → 解决方案2
```

**验证清单**：
- [ ] 每个Skills是否有前辈对比
- [ ] 前辈对比是否完整（表格+解决的问题）
- [ ] 前辈是否是功能相似的Skills

**输出**：
```
前辈对比验证：
- 有前辈对比：X个
- 无前辈对比：Y个（已标记待补充）
```

### 4. 高星Skills对比（P19规则）
**目标**：单独板块对比高星参考库

**高星参考库**：
- [ ] html-anything⭐5,321
- [ ] claude-code-plugins-plus-skills⭐2,254
- [ ] markdown-viewer/skills⭐2,863
- [ ] awesome-copilot-agents⭐525
- [ ] awesome-claude-skills⭐353

**对比表格**：
| 新Skill | Stars | vs html-anything⭐5321 | vs claude-code-plugins-plus-skills⭐2254 | 改进空间 |

**验证清单**：
- [ ] 是否有单独的高星Skills对比板块
- [ ] 是否与前辈对比不重复
- [ ] 是否包含高星参考库
- [ ] 是否有改进建议

**输出**：
```
高星Skills对比：
- 有单独板块：✅
- 与前辈对比不重复：✅
- 包含高星参考库：X个
- 有改进建议：✅
```

## ✅ 执行确认

**Skills报告生成完成后，必须输出以下确认信息**：
```
📊 Skills报告生成完成确认
====================
1. 内容详略：完整格式X个，简写格式Y个
2. 分类：第一类X个，第二类Y个，第三类Z个...
3. 前辈对比：有X个，无Y个（已标记待补充）
4. 高星对比：有单独板块✅，不重复✅

总计：Skills报告生成完成，共X个Skills，Y个类别
```

## ⚠️ 异常处理

**如果某个Skills信息不完整**：
1. 标记为"待补充"
2. 尝试从其他来源获取
3. 如果无法获取，跳过该Skills

**如果前辈对比找不到**：
1. 搜索GitHub上功能相似的Skills
2. 搜索已知的高星Skills
3. 如果仍找不到，标记为"前辈对比待补充"

## 📝 执行记录

**必须保存到**：`D:/openclaw-hermes/data/daily/YYYY-MM-DD/skills_report_log.json`

**记录内容**：
```json
{
  "date": "2026-05-30",
  "content_detail": {"complete": 10, "brief": 2},
  "classification": {"type1": 2, "type2": 2, "type3": 2, "type4": 1, "type5": 1, "type6": 1},
  "predecessor_comparison": {"has": 8, "missing": 1},
  "high_star_comparison": {"has_separate_section": true, "not_duplicate": true}
}
```
