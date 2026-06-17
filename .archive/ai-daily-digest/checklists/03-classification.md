# 分类执行清单

## 📋 执行前确认
- [ ] 数据验证已完成
- [ ] 已获取verification_log.json
- [ ] 已过滤非今日数据
- [ ] **已建立已分类项目字典（去重机制）**

## 🔍 分类清单

### 0. 去重机制（必须执行，最高优先级）
**目标**：确保同一个项目只被分类一次，只出现在一个板块

**去重流程**：
```python
# 建立已分类项目字典
classified_projects = {}  # {project_name: {"category": "agent/skill/component/mcp", "sub_category": "all_round/specialized/..."}}

def classify_with_dedup(project):
    """分类前先检查是否已分类"""
    project_name = project["name"]
    
    # 检查是否已分类
    if project_name in classified_projects:
        print(f"⚠️ 项目 {project_name} 已分类为 {classified_projects[project_name]['category']}，跳过重复分类")
        return classified_projects[project_name]
    
    # 执行分类判断流程
    category = classify_project(project)
    
    # 记录分类结果
    classified_projects[project_name] = {
        "category": category,
        "sub_category": get_sub_category(project, category),
        "source": project.get("source", "unknown"),
        "classification_time": datetime.now().isoformat()
    }
    
    return classified_projects[project_name]
```

**验证清单**：
- [ ] 是否建立已分类项目字典
- [ ] 分类前是否检查项目是否已分类
- [ ] 重复项目是否被跳过
- [ ] 是否记录分类来源（哪个搜索查询）

**输出**：
```
去重统计：
- 总项目数：X
- 去重后：Y个
- 重复项目：Z个（已跳过）
```

### 1. 分类判断流程（必须执行）
**目标**：将每个项目分类为Agent/Skills/组件

**判断流程（按顺序执行）**：
```
Step 1: 描述含"skill(s)" → 📚 Skills
Step 2: 主要是.md文件（.md > .py） → 📚 Skills
Step 3: 描述含"mcp server"/"model context protocol" → 🔌 MCP
Step 4: 描述含"for ai agents"/"for claude"/"let ai agents" → 🧩 Agent组件
Step 5: 描述含"ai agent"/"agent for"/能独立执行任务 → 🤖 Agent
Step 6: 以上都不满足 → 🧩 Agent组件
```

**验证清单**：
- [ ] 每个项目是否执行了Step 1-6流程
- [ ] 每个项目的分类依据是否记录
- [ ] 分类结果是否与描述关键词匹配

**输出**：
```
分类结果：
- 🤖 Agent：X个
- 📚 Skills：Y个
- 🧩 组件：Z个
- 🔌 MCP：W个
```

### 2. Agent细分（必须）
**目标**：将Agent细分为全能Agent和专精Agent

**判断标准**：
- **全能Agent**：通用型平台，能处理任意类型任务（Claude Code、Cursor、OpenHands、Hermes、OpenClaw）
- **专精Agent**：面向特定领域的Agent（DB-GPT=数据、HolmesGPT=SRE、html-anything=设计）

**验证清单**：
- [ ] 全能Agent：是否真的是通用型（不限定任务领域）
- [ ] 专精Agent：是否真的是垂直领域（功能限定在某个领域）
- [ ] 是否有误判（有API≠全能，平台≠全能）

**输出**：
```
Agent细分结果：
- 🤖 全能Agent：X个
- 🤖 专精Agent：Y个
```

### 3. Skills细分（必须）
**目标**：将Skills细分为6类

**6类Skills**：
1. **减少token消耗**：压缩输入、精简上下文、智能路由（token-saver、context-budget、prompt-optimizer）
2. **约束行为**：限制Agent行为范围、安全防护、流程规范（safety-guard、security-review、process-thinking）
3. **增加功能**：扩展Agent能力、添加新工具（content-search-organizer、url-summary、instructor）
4. **科研辅助**：论文阅读、文献检索、实验设计（ARIS系列、deep-research、research-lit）
5. **检测正常工作**：验证/监控/审计类skill，确保Agent输出质量（verification-loop、skill-stocktake、canary-watch、cache-audit、security-scan）
6. **补充类/其他**：独立于前5类之外的skills、资源索引集合（awesome-*系列、hermes-atlas、skill-scout、hermes-agent）

**验证清单**：
- [ ] 每个Skills是否归入正确的类别
- [ ] 每个Skills的描述是否与类别匹配
- [ ] 是否有遗漏的类别

**输出**：
```
Skills细分结果：
- 第一类（减少token）：X个
- 第二类（约束行为）：Y个
- 第三类（增加功能）：Z个
- 第四类（科研辅助）：W个
- 第五类（检测正常）：V个
- 第六类（补充类）：U个
```

### 4. 交叉验证（必须）
**目标**：验证分类是否一致，确保无重复

**验证方法**：
```python
# 检查同一个项目在不同搜索结果中的分类是否一致
for project in all_projects:
    classifications = get_classifications(project["name"])
    if len(set(classifications)) > 1:
        print(f"⚠️ 项目 {project['name']} 分类不一致：{classifications}")
        # 重新执行分类判断流程
        new_class = reclassify(project)
        print(f"  重新分类为：{new_class}")

# 检查是否有重复项目出现在不同板块
def check_duplicates_in_sections(report_content):
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
```

**验证清单**：
- [ ] 同一项目：在不同搜索结果中的分类是否一致
- [ ] 不一致项目：是否重新分类
- [ ] 重新分类结果：是否合理
- [ ] **报告中是否有重复项目出现在不同板块**

**输出**：
```
交叉验证结果：
- 一致：X个项目
- 不一致：Y个项目（已重新分类）
- 重复项目：Z个（已处理）
```

## ✅ 执行确认

**分类完成后，必须输出以下确认信息**：
```
📊 分类完成确认
====================
1. 总项目数：X
2. 去重后：Y个
3. 🤖 Agent：Z个（全能W个，专精V个）
4. 📚 Skills：U个（第一类T个，第二类S个...）
5. 🧩 组件：R个
6. 🔌 MCP：Q个
7. 交叉验证：P个项目一致，O个项目重新分类
8. 重复检查：N个重复项目已处理

总计：分类X个项目，去重后Y个，Agent:Z，Skills:U，组件:R，MCP:Q
```

## ⚠️ 异常处理

**如果分类不一致**：
1. 重新执行分类判断流程
2. 记录重新分类的原因
3. 使用重新分类的结果

**如果发现重复项目**：
1. 检查重复原因（搜索阶段/分类阶段/报告阶段）
2. 使用第一次分类的结果
3. 跳过重复分类
4. 记录重复项目信息

**如果分类不确定**：
1. 标记为"待确认"
2. 查看GitHub仓库结构
3. 查看描述关键词
4. 如果仍不确定，归入"组件"

## 📝 执行记录

**必须保存到**：`D:/openclaw-hermes/data/daily/YYYY-MM-DD/classification_log.json`

**记录内容**：
```json
{
  "date": "2026-05-30",
  "total_projects": 50,
  "after_dedup": 45,
  "duplicate_projects": 5,
  "agents": {"total": 15, "all_round": 7, "specialized": 8},
  "skills": {"total": 20, "type1": 5, "type2": 4, "type3": 3, "type4": 2, "type5": 3, "type6": 3},
  "components": 10,
  "mcp": 5,
  "cross_verification": {"consistent": 45, "inconsistent": 5, "reclassified": 5, "duplicates_found": 3}
}
```
