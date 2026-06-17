# 流程思维 Skill

拆分事件，将任务分成细致的环节，在执行任务前进行分析和规划。

## 🎯 核心定位

**用途**：在执行任务前进行流程分析和拆分  
**目标**：将复杂任务分解为可执行的环节  
**价值**：提高任务执行效率和质量

## 🔄 核心流程

```
接收任务 → 分析任务 → 拆分环节 → 定义流程 → 执行任务 → 复盘优化
```

## 🚀 快速开始

### 1. 拆分任务

```python
from client import decompose_task

# 拆分学习任务
result = decompose_task("学习Python", task_type="learning")
print(result)

# 自动识别任务类型
result = decompose_task("学习机器学习")
print(result)
```

### 2. 获取流程模板

```python
from client import get_process_template

# 获取学习模板
template = get_process_template("learning")
print(template)

# 获取开发模板
template = get_process_template("development")
print(template)
```

### 3. 创建自定义流程

```python
from client import create_custom_process

steps = [
    {
        "step": 1,
        "name": "准备",
        "description": "准备工作",
        "tasks": ["收集资料", "制定计划"],
        "estimated_time": "30分钟",
        "dependencies": []
    },
    {
        "step": 2,
        "name": "执行",
        "description": "执行任务",
        "tasks": ["按计划执行", "记录进度"],
        "estimated_time": "60分钟",
        "dependencies": [1]
    }
]

process = create_custom_process("自定义流程", steps)
print(process)
```

### 4. 格式化流程

```python
from client import format_process

# 文本格式
text = format_process(process, format="text")
print(text)

# JSON格式
json_str = format_process(process, format="json")
print(json_str)

# Markdown格式
md = format_process(process, format="markdown")
print(md)
```

## 📝 预定义流程

### 学习流程
```
1. 预习 → 2. 听课 → 3. 练习 → 4. 复习 → 5. 考试 → 6. 复盘 → 7. 单元测验
```

### 开发流程
```
1. 需求分析 → 2. 设计 → 3. 编码 → 4. 测试 → 5. 部署 → 6. 监控 → 7. 优化
```

### 写作流程
```
1. 选题 → 2. 大纲 → 3. 初稿 → 4. 修改 → 5. 校对 → 6. 发布 → 7. 反馈
```

## 🎯 使用场景

### 场景1: 学习新知识
```
用户: "我要学习Python"
AI: [流程思维] 让我帮你拆分学习流程
AI: [输出] 学习流程：预习 → 听课 → 练习 → 复习 → 考试 → 复盘 → 单元测验
用户: "好的，从预习开始"
AI: [执行] 开始预习...
```

### 场景2: 开发新功能
```
用户: "我要开发一个登录功能"
AI: [流程思维] 让我帮你拆分开发流程
AI: [输出] 开发流程：需求分析 → 设计 → 编码 → 测试 → 部署 → 监控 → 优化
用户: "好的，从需求分析开始"
AI: [执行] 开始需求分析...
```

### 场景3: 写文章
```
用户: "我要写一篇技术博客"
AI: [流程思维] 让我帮你拆分写作流程
AI: [输出] 写作流程：选题 → 大纲 → 初稿 → 修改 → 校对 → 发布 → 反馈
用户: "好的，从选题开始"
AI: [执行] 开始选题...
```

## 🔧 API参考

### 核心函数

#### `decompose_task(task_description, task_type=None) -> Dict`
拆分任务为多个环节

**参数**：
- `task_description`: 任务描述
- `task_type`: 任务类型（learning/development/writing/custom）

**返回**：流程定义

#### `get_process_template(process_type) -> Dict`
获取预定义流程模板

**参数**：
- `process_type`: 流程类型（learning/development/writing）

**返回**：流程模板

#### `create_custom_process(name, steps) -> Dict`
创建自定义流程

**参数**：
- `name`: 流程名称
- `steps`: 环节列表

**返回**：自定义流程

#### `format_process(process, format="text") -> str`
格式化流程

**参数**：
- `process`: 流程定义
- `format`: 输出格式（text/json/markdown）

**返回**：格式化的流程

## 💡 关键价值

1. **结构化思维**：将复杂任务分解为可执行的环节
2. **提高效率**：按流程执行，避免遗漏
3. **质量保证**：每个环节都有明确的标准
4. **持续优化**：根据反馈不断改进流程
5. **知识积累**：沉淀最佳实践

## 📚 相关文件

- **SKILL.md**: 技能说明
- **client.py**: Python客户端模块
- **test_process_thinking.py**: 测试脚本
