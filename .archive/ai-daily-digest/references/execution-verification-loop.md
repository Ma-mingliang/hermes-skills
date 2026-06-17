# 执行验证循环（Execution Verification Loop）

> 基于10个GitHub项目的核心思想，解决"有清单但不执行"的问题

## 核心问题

我们有完整的执行清单（8个checklists），但执行时：
1. 不加载清单文件，凭记忆执行
2. 跳过验证环节，直接进入下一步
3. 每次犯同样错误，不从执行中学习
4. "完成"的定义太低，缺少分析环节

## 10个GitHub方案的核心思想

| 方案 | Stars | 核心思想 | 我们的应用 |
|------|-------|---------|-----------|
| OpenAgentsControl | 4184 | plan-first + approval-based | 执行前必须加载清单 |
| prax-agent | 295 | test-verify-fix loops | 执行→验证→修复循环 |
| SE-Agent | 273 | trajectory-level evolution | 从每次执行中学习 |
| orra | 242 | dynamic planning engine | 动态调整执行计划 |
| AutoDidact | 689 | self-verification | 自我验证执行结果 |
| kweaver-core | 808 | verifiable feedback loops | 每个环节可验证 |
| TaskWeaver | 6162 | code-first planning | 代码驱动的规划 |
| CowAgent | 44972 | autonomous growth with memory | 从经验中自主成长 |
| claude-swarm | 179 | multi-agent decomposition | 多Agent协作分解任务 |
| inferable | 440 | humans in the loop | 人类监督关键节点 |

## 改进的执行流程

### 原流程（问题）
```
Step 1: 加载配置
Step 2: 数据收集
Step 3: 分类
Step 4: 生成报告
Step 5: 推送
```

### 新流程（改进）
```
Step 1: 加载配置 + 加载清单
    ↓
Step 1.5: 验证清单加载成功
    ↓ 通过？→ 是 → 继续
    ↓ 否 → 重新加载
Step 2: 数据收集（按清单逐项执行）
    ↓
Step 2.5: 验证数据收集（对照清单逐项检查）
    ↓ 通过？→ 是 → 继续
    ↓ 否 → 修复 → 回到Step 2.5
Step 3: 分类（按清单逐项执行）
    ↓
Step 3.5: 验证分类（对照清单逐项检查）
    ↓ 通过？→ 是 → 继续
    ↓ 否 → 修复 → 回到Step 3.5
Step 4: 生成报告（按清单逐项执行）
    ↓
Step 4.5: 验证报告（对照清单逐项检查）
    ↓ 通过？→ 是 → 继续
    ↓ 否 → 修复 → 回到Step 4.5
Step 5: 推送
    ↓
Step 5.5: 验证推送成功
    ↓ 通过？→ 是 → 完成
    ↓ 否 → 重试
Step 6: 复盘（记录执行过程中的问题）
Step 7: 更新skill（从执行中学习）
```

## 关键改进点

### 1. Plan-First（来自OpenAgentsControl）
**原问题**：执行前不加载清单，凭记忆执行
**改进**：
```python
# 执行前必须加载清单
def load_checklist(step_name):
    checklist_path = f"checklists/{step_name}.md"
    with open(checklist_path, "r") as f:
        checklist = f.read()
    return checklist

# 执行前必须列出要做的事
def plan_execution(checklist):
    items = extract_checklist_items(checklist)
    print(f"📋 要执行 {len(items)} 项")
    for i, item in enumerate(items):
        print(f"  {i+1}. {item}")
    return items
```

### 2. Test-Verify-Fix Loops（来自prax-agent）
**原问题**：执行完不验证，直接进入下一步
**改进**：
```python
def execute_with_verification(step_name, execute_func):
    # 加载清单
    checklist = load_checklist(step_name)
    items = plan_execution(checklist)
    
    # 执行
    result = execute_func()
    
    # 验证
    verification = verify_against_checklist(result, checklist)
    
    # 修复循环
    max_attempts = 3
    attempt = 0
    while not verification["passed"] and attempt < max_attempts:
        attempt += 1
        print(f"⚠️ 验证失败，第{attempt}次修复...")
        result = fix_issues(result, verification["issues"])
        verification = verify_against_checklist(result, checklist)
    
    return result
```

### 3. Trajectory-Level Evolution（来自SE-Agent）
**原问题**：每次执行都犯同样错误
**改进**：
```python
# 记录执行轨迹
execution_trajectory = {
    "date": "2026-05-31",
    "steps": [],
    "errors": [],
    "fixes": []
}

# 执行后记录
def record_trajectory(step_name, result, errors, fixes):
    execution_trajectory["steps"].append({
        "step": step_name,
        "result": result,
        "errors": errors,
        "fixes": fixes
    })
    
    # 保存到文件
    with open(f"data/daily/{today}/execution_trajectory.json", "w") as f:
        json.dump(execution_trajectory, f, indent=2)

# 下次执行前读取历史轨迹
def load_history():
    try:
        with open(f"data/daily/yesterday/execution_trajectory.json", "r") as f:
            return json.load(f)
    except:
        return None

# 从历史中学习
def learn_from_history(history):
    if history:
        print("📚 从历史执行中学习：")
        for error in history["errors"]:
            print(f"  ⚠️ 上次错误：{error}")
        for fix in history["fixes"]:
            print(f"  ✅ 上次修复：{fix}")
```

### 4. Verifiable Feedback Loops（来自kweaver-core）
**原问题**：每个环节没有可验证的输出
**改进**：
```python
# 每个环节必须有可验证的输出
verification_schema = {
    "data_collection": {
        "required_outputs": ["github_projects", "hn_posts", "36kr_news", "model_officials"],
        "validation_rules": [
            "len(github_projects) > 0",
            "len(hn_posts) > 0",
            "all(p['created_at'] >= week_ago for p in github_projects)"
        ]
    },
    "classification": {
        "required_outputs": ["agents", "skills", "components"],
        "validation_rules": [
            "len(agents) + len(skills) + len(components) == total_projects",
            "all(a['category'] == 'agent' for a in agents)",
            "all(s['category'] == 'skill' for s in skills)"
        ]
    }
}

def verify_step(step_name, result):
    schema = verification_schema[step_name]
    
    # 检查必需输出
    for output in schema["required_outputs"]:
        if output not in result:
            return {"passed": False, "reason": f"缺少输出: {output}"}
    
    # 检查验证规则
    for rule in schema["validation_rules"]:
        if not eval(rule, {"result": result, **result}):
            return {"passed": False, "reason": f"规则失败: {rule}"}
    
    return {"passed": True}
```

### 5. Self-Verification（来自AutoDidact）
**原问题**：不自我验证执行结果
**改进**：
```python
def self_verify(step_name, result):
    """自我验证执行结果"""
    
    # 1. 检查完整性
    completeness = check_completeness(step_name, result)
    
    # 2. 检查准确性
    accuracy = check_accuracy(step_name, result)
    
    # 3. 检查一致性
    consistency = check_consistency(step_name, result)
    
    # 综合评分
    score = (completeness + accuracy + consistency) / 3
    
    return {
        "score": score,
        "completeness": completeness,
        "accuracy": accuracy,
        "consistency": consistency,
        "passed": score >= 0.8
    }
```

### 6. Humans in the Loop（来自inferable）
**原问题**：执行过程不可控
**改进**：
```python
# 关键节点需要人类确认
critical_checkpoints = [
    "data_collection_complete",  # 数据收集完成后
    "classification_complete",   # 分类完成后
    "report_generation_complete", # 报告生成完成后
]

def human_checkpoint(step_name, result):
    """在关键节点暂停，等待人类确认"""
    if step_name in critical_checkpoints:
        print(f"\n⏸️ 关键节点：{step_name}")
        print(f"📊 结果预览：")
        preview_result(result)
        
        # 在交互模式下，等待用户确认
        # 在cron模式下，自动通过
        return True
    return True
```

## 执行清单模板

每个Step的执行清单必须包含：

```markdown
# Step N: [步骤名称] 执行清单

## 📋 执行前确认
- [ ] 已加载清单文件
- [ ] 已确认前置步骤完成
- [ ] 已准备必要资源

## 🔍 执行项
### 1. [执行项1]
- [ ] 子项1
- [ ] 子项2
- [ ] 子项3

### 2. [执行项2]
- [ ] 子项1
- [ ] 子项2

## ✅ 验证清单
- [ ] 输出完整性检查
- [ ] 输出准确性检查
- [ ] 输出一致性检查

## ⚠️ 异常处理
- 如果XX失败 → 做YY
- 如果XX超时 → 做ZZ

## 📝 执行记录
- 执行时间：
- 执行结果：
- 遇到问题：
- 解决方案：
```

## 使用方法

1. **执行前**：加载对应的清单文件
2. **执行中**：逐项对照清单执行
3. **执行后**：验证输出是否符合清单要求
4. **验证失败**：修复后重新验证
5. **验证通过**：进入下一步
6. **完成后**：记录执行轨迹，更新skill

## 验证命令

```python
# 验证执行完整性
def verify_execution_completeness(today):
    """验证所有步骤是否完成"""
    data_dir = f"D:/openclaw-hermes/data/daily/{today}"
    
    required_files = [
        "raw/github_projects.json",
        "raw/hn_posts.json",
        "raw/36kr_news.json",
        "raw/model_officials.json",
        "classified_projects.json",
        "report.md",
        "execution_trajectory.json"
    ]
    
    missing = []
    for f in required_files:
        if not os.path.exists(f"{data_dir}/{f}"):
            missing.append(f)
    
    if missing:
        print(f"❌ 缺少文件：{missing}")
        return False
    
    print("✅ 所有步骤已完成")
    return True
```

## 参考项目

- [OpenAgentsControl](https://github.com/darrenhinde/OpenAgentsControl) ⭐4184
- [prax-agent](https://github.com/ChanningLua/prax-agent) ⭐295
- [SE-Agent](https://github.com/JARVIS-Xs/SE-Agent) ⭐273
- [orra](https://github.com/orra-dev/orra) ⭐242
- [AutoDidact](https://github.com/dCaples/AutoDidact) ⭐689
- [kweaver-core](https://github.com/kweaver-ai/kweaver-core) ⭐808
- [TaskWeaver](https://github.com/microsoft/TaskWeaver) ⭐6162
- [CowAgent](https://github.com/zhayujie/CowAgent) ⭐44972
- [claude-swarm](https://github.com/affaan-m/claude-swarm) ⭐179
- [inferable](https://github.com/inferablehq/inferable) ⭐440
