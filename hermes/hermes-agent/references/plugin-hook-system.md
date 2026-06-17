# Hermes Plugin Hook 机制

> 让功能在每个LLM turn自动触发，不需要用户手动加载。

## 两种机制对比

| 机制 | 触发方式 | 位置 | 适合场景 |
|------|---------|------|---------|
| **Skill** | 用户输入触发关键词 | `~/.hermes/skills/` | 按需加载的任务 |
| **Plugin** | 每个LLM turn自动触发 | `~/.hermes/plugins/` | 始终运行的钩子 |

## 可用的Hook事件

| Hook | 触发时机 | 能做什么 |
|------|---------|---------|
| `pre_llm_call` | LLM调用前 | 注入上下文到user message末尾（ephemeral，不污染system prompt） |
| `pre_tool_call` | 工具调用前 | 拦截工具调用，返回block消息 |
| `post_tool_call` | 工具调用后 | 处理工具输出 |

## 创建Plugin的步骤

### 1. 创建目录
```bash
mkdir -p ~/.hermes/plugins/<plugin-name>/
```

### 2. 创建 plugin.yaml
```yaml
name: <plugin-name>
version: 1.0.0
description: "描述"
author: "作者"
kind: standalone
hooks:
  - pre_llm_call  # 声明要使用的hook
```

### 3. 创建 hooks.py
```python
def on_pre_llm_call(*, session_id="", user_message="",
                    conversation_history=None, is_first_turn=False,
                    model="", platform="", sender_id="", **kwargs) -> dict:
    """返回 {"context": "..."} 会被append到user message末尾"""
    return {"context": "要注入的内容"}

def register_hooks(ctx) -> None:
    ctx.register_hook("pre_llm_call", on_pre_llm_call)
```

### 4. 创建 __init__.py
```python
import importlib.util, sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

def _load_register_hooks():
    hooks_path = _repo_root / "hooks.py"
    module_name = f"{__name__}._hooks"
    spec = importlib.util.spec_from_file_location(module_name, hooks_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.register_hooks

register_hooks = _load_register_hooks()

def register(ctx) -> None:
    register_hooks(ctx)
```

### 5. 重启Gateway
```bash
hermes gateway restart
```

## 已知Plugin示例

| Plugin | 功能 | Hook |
|--------|------|------|
| `hermes-time-perception` | 注入当前时间标签 | pre_llm_call |
| `reasoning-trace-hook` | 注入推理追踪指令 | pre_llm_call |

## 关键特性

- **ephemeral**：注入内容不进入system prompt，不影响prompt cache
- **自动发现**：Hermes自动扫描 `~/.hermes/plugins/` 目录
- **可组合**：多个plugin可以同时使用同一个hook
- **可配置**：通过config.yaml的 `plugins:` 部分配置信任级别和LLM访问

## Plugin的LLM访问

Plugin可以通过 `ctx.llm` 调用LLM：
- `ctx.llm.complete(messages, ...)` — 聊天补全
- `ctx.llm.complete_structured(instructions=..., json_schema=...)` — 结构化输出

需要在config.yaml中配置信任：
```yaml
plugins:
  entries:
    my-plugin:
      llm:
        allow_provider_override: true
        allowed_providers: [openrouter, anthropic]
```

## Shell Hook（替代方案）

除了Python Plugin，还可以用Shell Hook：

```yaml
# config.yaml
hooks:
  pre_llm_call:
    - command: "python3 /path/to/hook.py"
      timeout: 5
```

Shell Hook通过stdin接收JSON，stdout返回JSON。

## 参考项目

- [gejifeng/hermes-time-perception-extension](https://github.com/gejifeng/hermes-time_perception-extension) — pre_llm_call hook示例
- [piiiico/hermes-agentlair](https://github.com/piiiico/hermes-agentlair) — AgentLair集成，persistent identity + lifecycle hooks
