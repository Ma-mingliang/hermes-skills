# Reasoning Trace Skill

记录AI推理过程，用于skill修改调整，支持任务→skill流程，添加思维验证功能。

## 🎯 核心定位

**用途**：用于skill的修改调整  
**目标**：以任务导向的更新skill  
**范围**：压缩到skill修改调整这个领域内

## 🔄 核心流程

```
执行任务 → 记录推理过程 → 思维验证 → 用户发现问题 → 用户给出修改意见 → 更新skill
    ↓
hermes-skill-factory捕获工作流 → 自动生成skill
    ↓
用户审查skill → 给出修改意见 → 更新skill
    ↓
后续任务 → 使用更新后的skill → 执行任务
```

## 🚀 快速开始

### 1. 记录推理过程

```python
from client import start_trace, trace_step, end_trace

# 开始记录
task_id = start_trace("task_001", "执行某个任务")

# 记录推理步骤
trace_step("reasoning", "我需要先检查...")
trace_step("decision", "我决定使用...")
trace_step("assumption", "我假设...")

# 结束记录
result = end_trace("success")
```

### 2. 思维验证（新增）

```python
from client import verify_decision, check_consistency

# 在做决策前进行验证
verify_decision(
    decision="ARIS是Agent",
    verification_questions=[
        "有没有反例？",
        "一定是对的吗？",
        "如果错了会怎样？"
    ]
)

# 检查是否与之前的分析一致
check_consistency(
    current_decision="ARIS是Agent",
    previous_analysis="ARIS = Skills"
)
```

### 3. 关联任务和skill

```python
from client import link_task_to_skill, get_skill_traces

# 关联任务和skill
link_task_to_skill(task_id, "my_skill")

# 获取skill的生成过程
skill_traces = get_skill_traces("my_skill")
```

### 4. 保存skill修改意见

```python
from client import save_skill_modification, get_skill_modifications

# 保存skill修改意见
save_skill_modification(
    skill_name="my_skill",
    user_feedback="这个skill应该先检查X",
    related_task_id="task_001"
)

# 获取skill修改意见
modifications = get_skill_modifications("my_skill")
```

### 5. skill版本管理

```python
from client import save_skill_version, rollback_skill, get_skill_diff

# 保存skill版本
save_skill_version("my_skill", version="1.0")

# 回滚到之前的版本
rollback_skill("my_skill", version="1.0")

# 查看修改差异
diff = get_skill_diff("my_skill", "1.0", "1.1")
```

### 6. 清理功能

```python
from client import cleanup_traces, get_storage_stats

# 清理30天前的trace
cleanup_traces(keep_days=30)

# 获取存储统计
stats = get_storage_stats()
```

## 📝 使用场景

### 场景1: 思维验证

```
AI准备生成回答："ARIS有CLI但是Agent"
    ↓
思维验证：检查是否与分析一致
    ↓
发现不一致：分析说ARIS=Skills，但回答说ARIS=Agent
    ↓
调整回答："ARIS有CLI但是Skills"
    ↓
记录验证过程到Reasoning Trace
```

### 场景2: 任务→skill优化

```
用户: "执行这个任务"
AI: [执行任务，记录推理过程]
AI: [hermes-skill-factory生成skill]
用户: "这个skill有问题，应该先检查X"
AI: [保存修改意见，更新skill]
用户: "下次执行类似任务时，使用更新后的skill"
AI: [使用更新后的skill执行任务]
```

### 场景3: skill迭代优化

```
用户: "这个skill的推理过程怎么样？"
AI: [回放skill的生成过程]
用户: "第3步有问题，应该先检查Y"
AI: [保存修改意见，更新skill]
用户: "查看修改历史"
AI: [展示skill的修改历史]
```

## 📊 存储结构

```
~/.hermes/
├── traces/                          # 推理过程存储
│   ├── YYYY-MM-DD/                  # 按日期组织
│   │   ├── task_XXX.json           # 推理过程文件
│   │   └── ...
│   └── index.json                  # 索引文件
├── skills/
│   ├── reasoning-trace/
│   │   ├── SKILL.md                # 技能说明
│   │   ├── client.py               # 客户端模块
│   │   ├── cleanup.py              # 清理脚本
│   │   └── modifications/          # 修改意见
│   │       ├── YYYY-MM-DD.json     # 任务修改意见
│   │       └── skill_YYYY-MM-DD.json  # skill修改意见
│   └── <skill_name>/
│       ├── SKILL.md                # skill内容
│       └── versions/               # 版本历史
│           ├── 1.0/
│           ├── 1.0.json
│           └── ...
```

## 💡 关键价值

1. **完整闭环**：任务→skill→修改→更新→任务
2. **可追溯**：记录skill的生成过程和修改历史
3. **可改进**：用户可以参与skill的优化过程
4. **可回滚**：支持回滚到之前的版本
5. **思维验证**：在做决策前进行验证，避免错误
6. **高效**：不输出token，节省成本

## 🔧 API参考

### ReasoningTrace 类

#### 推理过程相关
- `start(task_id=None, description="") -> str` - 开始记录
- `step(step_type, content, confidence=1.0, metadata=None) -> int` - 记录步骤
- `end(result="success") -> Dict` - 结束记录
- `get(task_id) -> Optional[Dict]` - 获取trace数据
- `replay(task_id, format="text") -> str` - 回放推理过程

#### 思维验证相关（新增）
- `verify_decision(decision, verification_questions) -> Dict` - 验证决策
- `check_consistency(current_decision, previous_analysis) -> Dict` - 检查一致性

#### 任务→skill相关
- `link_to_skill(task_id, skill_name) -> bool` - 关联任务和skill
- `get_skill_traces(skill_name) -> List[Dict]` - 获取skill的生成过程

#### skill修改意见相关
- `save_skill_modification(skill_name, user_feedback, related_task_id=None) -> Dict` - 保存skill修改意见
- `get_skill_modifications(skill_name=None) -> List[Dict]` - 获取skill修改意见

#### skill版本管理相关
- `save_skill_version(skill_name, version, description="") -> bool` - 保存skill版本
- `rollback_skill(skill_name, version) -> bool` - 回滚skill
- `get_skill_diff(skill_name, version1, version2) -> Dict` - 获取版本差异

#### 清理相关
- `cleanup(keep_days=30) -> Dict` - 清理旧的trace文件
- `get_storage_stats() -> Dict` - 获取存储统计信息

## 🧹 清理策略

- **默认保留时间**: 30天
- **自动清理**: 每天凌晨3点
- **手动清理**: `cleanup_traces(keep_days=30)`

## 📚 相关文件

- **SKILL.md**: 技能说明
- **client.py**: Python客户端模块
- **cleanup.py**: 清理脚本
- **test_reasoning_trace.py**: 测试脚本
