# 去重机制实现指南（2026-05-31）

## 问题背景
同一个项目被分类两次，出现在不同板块。根因：搜索→分类→报告三个阶段都没有去重。

## 思维追踪法诊断

### 环节1：搜索阶段
- **实际**：多个搜索查询（ai agent, agent skills, mcp server等）返回相同项目
- **预期**：每个项目只记录一次
- **差异**：没有去重集合

### 环节2：分类阶段
- **实际**：对每个搜索结果单独分类，不检查是否已分类
- **预期**：分类前先查已分类字典
- **差异**：可能重复分类

### 环节3：报告阶段
- **实际**：凭印象或搜索来源决定板块
- **预期**：查分类标签决定板块
- **差异**：可能重复写入

## 三阶段去重实现

### 1. 搜索阶段去重
```python
collected_projects = set()

def collect_with_dedup(project):
    project_name = project["name"]
    if project_name in collected_projects:
        return None
    collected_projects.add(project_name)
    return project
```

### 2. 分类阶段去重
```python
classified_projects = {}  # {name: {"category": ..., "sub_category": ..., "source": ...}}

def classify_with_dedup(project):
    project_name = project["name"]
    if project_name in classified_projects:
        return classified_projects[project_name]
    
    category = classify_project(project)  # 执行Step 1-6流程
    classified_projects[project_name] = {
        "category": category,
        "sub_category": get_sub_category(project, category),
        "source": project.get("source", "unknown"),
        "classification_time": datetime.now().isoformat()
    }
    return classified_projects[project_name]
```

### 3. 报告阶段验证
```python
def check_report_duplicates(report_content):
    projects_in_sections = {}
    sections = report_content.split('# ')
    for section in sections:
        section_name = section.split('\n')[0].strip()[:50]
        project_names = extract_project_names(section)
        for name in project_names:
            if name not in projects_in_sections:
                projects_in_sections[name] = []
            projects_in_sections[name].append(section_name)
    
    duplicates = {n: s for n, s in projects_in_sections.items() if len(s) > 1}
    return duplicates
```

## 已更新的文件
1. `checklists/01-data-collection.md` — 第0节：搜索去重机制
2. `checklists/03-classification.md` — 第0节：分类去重机制
3. `checklists/04-agent-report.md` — 第0节：报告去重验证
4. `references/process-workflow.md` — ②.5 去重机制
5. `SKILL.md` — 分类流程前的去重机制 + P32 Pitfall
