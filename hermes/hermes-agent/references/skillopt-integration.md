# SkillOpt 集成指南

## 概述

SkillOpt 是微软开发的提示词优化工具，可以优化 Hermes skill 的自然语言提示词。

## 环境搭建

### 1. 克隆仓库
```bash
git clone https://github.com/microsoft/SkillOpt.git D:\openclaw-hermes\SkillOpt
```

### 2. 安装依赖
```bash
pip install skillopt
```

### 3. 配置 API
```bash
cp D:\openclaw-hermes\SkillOpt\.env.example D:\openclaw-hermes\SkillOpt\.env
# 编辑 .env，添加 MIMO_API_KEY
```

### 4. 创建环境目录
```bash
mkdir -p D:\openclaw-hermes\SkillOpt\skillopt\envs\<skill_name>
```

**注意：目录名必须用下划线，不能有连字符！**

### 5. 创建核心文件

#### __init__.py
```python
"""<Skill Name> benchmark environment for SkillOpt."""
from skillopt.envs.<skill_name>.adapter import <SkillName>Env
__all__ = ["<SkillName>Env"]
```

#### adapter.py
```python
from skillopt.envs.base import EnvAdapter
from skillopt.envs.<skill_name>.dataloader import <SkillName>Loader

class <SkillName>Env(EnvAdapter):
    def __init__(self, ...):
        self.dataloader = <SkillName>Loader(...)
    
    def setup(self, cfg):
        super().setup(cfg)
        self.dataloader.setup(cfg)
    
    def get_dataloader(self):
        return self.dataloader
    
    def build_env_from_batch(self, batch, **kwargs):
        return list(batch.payload or [])
    
    def build_train_env(self, batch_size, seed, **kwargs):
        batch = self.dataloader.build_train_batch(batch_size=batch_size, seed=seed, **kwargs)
        return self.build_env_from_batch(batch, **kwargs)
    
    def build_eval_env(self, split, seed=42, **kwargs):
        batch = self.dataloader.build_eval_batch(split=split, seed=seed, **kwargs)
        return self.build_env_from_batch(batch, **kwargs)
    
    def rollout(self, env_manager, skill_content, out_dir, **kwargs):
        # 实现 rollout 逻辑
        pass
    
    def reflect(self, results, skill_content, out_dir, **kwargs):
        # 实现 reflect 逻辑
        pass
    
    def get_task_types(self):
        return ["<skill_name>"]
```

#### dataloader.py
```python
from skillopt.datasets.base import SplitDataLoader

class <SkillName>Loader(SplitDataLoader):
    def load_split_items(self, split_path):
        # 实现数据加载逻辑
        pass
```

### 6. 注册环境

在 `scripts/train.py` 的 `_register_builtins()` 函数末尾添加：
```python
try:
    from skillopt.envs.<skill_name>.adapter import <SkillName>Env
    _ENV_REGISTRY["<skill_name>"] = <SkillName>Env
except ImportError:
    pass
```

### 7. 创建配置文件
```yaml
_base_: ../_base_/default.yaml

model:
  backend: azure_openai
  optimizer: mimo-v2.5-pro
  target: mimo-v2.5-pro
  optimizer_backend: openai_chat
  target_backend: openai_chat

train:
  num_epochs: 3
  train_size: <N>  # 必须等于 train 分割的样本数
  batch_size: 1

env:
  name: <skill_name>
  skill_init: skillopt/envs/<skill_name>/skills/initial.md
  split_mode: split_dir
  split_dir: data/<skill_name>
  data_path: data/<skill_name>/training_data.json
  out_root: outputs/<skill_name>
```

## 关键 Pitfalls

| 问题 | 解决 |
|------|------|
| Python 模块名不能有连字符 | 目录用下划线：`agent_daily_report` 不是 `agent-daily-report` |
| abstract method 缺失 | 必须实现 `get_task_types()` 方法 |
| rollout 方法签名错误 | 正确签名：`rollout(self, env_manager, skill_content, out_dir, **kwargs)` |
| reflect 方法签名错误 | 正确签名：`reflect(self, results, skill_content, out_dir, **kwargs)` |
| train_size 不匹配 | config 的 train_size 必须等于 train 分割的样本数 |
| JSON 解析失败 | reflect 函数需要 robust 的 JSON 解析 + fallback 机制 |
| 评估分数全为 0 | rollout 函数需要集成评估逻辑，返回 hard/soft 分数 |
| Edit 格式错误 | SkillOpt 期望 `{"op": "append|insert_after|replace|delete", "content": "...", "target": "..."}` 而非 `{"operation": "add", "old_text": "...", "new_text": "..."}` |
| patches=0 | reflect 函数调用了 LLM 但没有生成 patches → 检查 LLM 响应内容，添加 fallback |
| .env 加载失败 | 移除 .env 文件中的 `export` 前缀，Python 的 `os.environ` 不解析 `export` |

## 评估维度（推荐 4 个）

MiMo v2.5 Pro 无法可靠处理 12 维评估（返回空或全 0.50 默认值）。推荐使用 4 个核心维度：

| 维度 | 权重 | 说明 |
|------|------|------|
| completeness | 30% | 是否覆盖所有必要规则（合并 relevance, coverage, dedup, mcp, source） |
| specificity | 30% | 是否包含具体数值阈值和明确条件（合并 actionability） |
| clarity | 20% | 指令是否清晰无歧义 |
### MiMo 集成关键 Pitfall

**MiMo 空响应问题**: MiMo 默认开启 thinking 模式，导致 `content` 为空。必须在请求参数中添加：
```python
"thinking": {"type": "disabled"}
```

**评估函数 fallback**: 当 LLM 评估失败时（如 MiMo 返回空），使用规则评估作为 fallback：
- 检查数值阈值数量（star>=100 等）
- 检查操作规则数量（必须、不得、禁止等）
- 检查 section 数量
- 检查示例数量
- 长度奖励/惩罚

### 训练配置

```yaml
train:
  num_epochs: 3
  train_size: 4
  batch_size: 1

optimizer:
  learning_rate: 2
  min_learning_rate: 1
  lr_scheduler: cosine
  skill_update_mode: patch
  use_slow_update: true
```

### 评估维度（12 个）

基础：relevance, completeness, accuracy, actionability
新增：specificity, consistency, coverage, clarity, dedup_effectiveness, scoring_accuracy, mcp_validation, source_filtering

**注意**：如果使用 12 维评估，MiMo 会返回空内容，导致所有候选被拒绝（score=0.50）。

## 运行训练

```bash
cd D:\openclaw-hermes\SkillOpt

# 加载环境变量
set -a; source .env; set +a

# 运行训练
python scripts/train.py --config configs/<skill_name>/default.yaml

# 评估结果
python scripts/eval_only.py --config configs/<skill_name>/default.yaml --skill outputs/<skill_name>/best_skill.md
```

## 参考文件

- SkillOpt 仓库：https://github.com/microsoft/SkillOpt
- 配置模板：`D:\openclaw-hermes\SkillOpt\configs\_base_\default.yaml`
- 环境模板：`D:\openclaw-hermes\SkillOpt\skillopt\envs\_template\`
