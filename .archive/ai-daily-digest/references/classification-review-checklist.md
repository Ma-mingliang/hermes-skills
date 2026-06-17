# 分类审查执行清单（2026-05-31新增）

## 执行时机
Step 4（分类）完成后，Step 5（生成报告）之前

## 目的
验证分类结果的准确性，防止分类错误

## 审查项目

### 1. 已知误判案例检查
检查以下已知误判案例：

| 项目 | 错误分类 | 正确分类 | 原因 |
|------|---------|---------|------|
| ECC (⭐199K) | skill | component | 描述含"skills"但实际是Agent组件系统 |
| Dify (⭐143K) | mcp | agent_specialized | 描述含"workflow"但实际是工作流Agent平台 |
| hermes-agent (⭐174K) | component | agent_all_round | 描述"agent that grows"但代码未匹配 |
| superpowers (⭐212K) | component | skill | "agentic skills framework" = skills仓库非组件 |
| opencode (⭐167K) | component | agent_all_round | "open source coding agent" 被误判为框架 |

### 2. 高星项目人工确认
- 对Stars > 10,000的项目进行人工确认
- 检查项目描述和实际功能是否一致

### 3. 分类一致性检查
- 检查是否有同一个项目出现在多个板块
- 检查是否有重复分类的项目

### 4. 分类准确性检查
- 逐项检查每个项目的分类标签
- 验证分类是否符合P24规则（MCP > Agent组件 > Agent > Skills）

## 审查流程

```python
# 1. 加载分类结果
classified_projects = load_classified_projects()

# 2. 检查已知误判案例
for project in classified_projects:
    if project['name'] in KNOWN_MISCLASSIFICATIONS:
        correct = KNOWN_MISCLASSIFICATIONS[project['name']]
        if project['category'] != correct:
            log_correction(project, correct)

# 3. 检查高星项目
for project in classified_projects:
    if project['stars'] > 10000:
        verify_classification(project)

# 4. 记录审查结果
save_review_log(review_log)
```

## 验证清单
- [ ] 是否检查了已知误判案例表
- [ ] 是否对高星项目（>10K）进行人工确认
- [ ] 是否记录了修正日志
- [ ] 是否保存了审查结果

## 输出
- 审查报告（通过/修正项）
- 修正详情（如有）
- 审查统计（通过率）
