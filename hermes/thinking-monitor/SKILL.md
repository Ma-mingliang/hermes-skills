---
name: thinking-monitor
description: "思维监控skill - 监控Agent思维过程，追踪推理路径与决策点，识别思维偏差与错误，提供思维质量评估与优化建议。与reasoning-trace、process-thinking等skill配合使用。"
version: 1.0.0
category: hermes
tags: [thinking, monitor, reasoning, quality, bias, metacognition, decision-tracking]
---

# 思维监控 Skill (Thinking Monitor)

监控Agent的思维过程，追踪推理路径和决策点，识别思维偏差和错误，提供思维质量评估。

## 🎯 核心定位

**用途**：实时监控和事后审计Agent的思维过程  
**目标**：提升思维质量，减少推理错误和认知偏差  
**范围**：覆盖推理全过程——从初始判断到最终决策

## ⚡ 触发条件

**自动触发**：
- Agent执行复杂任务（5+工具调用）
- Agent做出关键决策
- 用户质疑Agent的推理过程
- Agent犯错后的事后分析
- 任务完成后自动复盘

**手动触发**：
- 用户说"检查思维"
- 用户说"评估推理质量"
- 用户说"看看我哪里想错了"
- 用户说"思维审计"

## 🔄 核心流程

```
思维过程 → 实时监控 → 维度评估 → 偏差检测 → 质量评分 → 优化建议
    ↑                                                          |
    └──────────────── 反馈闭环 ──────────────────────────────┘
```

## 📐 一、监控维度与指标体系

### 1.1 四大核心维度

| 维度 | 含义 | 权重 | 评估焦点 |
|------|------|------|----------|
| **逻辑严谨性** (Logical Rigor) | 推理链条是否完整、无跳跃 | 30% | 前提→推理→结论的完整性 |
| **信息充分性** (Information Adequacy) | 决策依据是否充分 | 25% | 证据收集、信息来源 |
| **偏差控制** (Bias Control) | 是否受认知偏差影响 | 25% | 常见偏差模式检测 |
| **效率适配** (Efficiency Fit) | 思维过程与任务复杂度匹配 | 20% | 过度/不足分析 |

### 1.2 细化指标

#### 逻辑严谨性指标
- **推理跳跃检测**：结论是否跳过必要中间步骤（Jump Threshold: 2+ missing steps）
- **前提明确性**：假设是否被显式声明（Explicit Ratio: 显式前提/总前提数）
- **一致性检查**：前后推理是否自洽（Contradiction Count）
- **因果链完整性**：因果推断是否有明确链条（Chain Depth）

#### 信息充分性指标
- **搜索深度**：信息搜索是否覆盖多源（Source Diversity: 单一源 vs 多源验证）
- **验证密度**：关键事实是否经过验证（Verification Ratio）
- **盲区识别**：是否明确标注未知领域（Unknown Declaration Rate）
- **时效性检查**：信息是否最新/上下文相关

#### 偏差控制指标（常见认知偏差）
| 偏差类型 | 检测信号 | 严重度 |
|----------|----------|--------|
| **确认偏差** (Confirmation Bias) | 倾向寻找支持性证据，忽略反面证据 | 🔴 高 |
| **锚定效应** (Anchoring) | 过度依赖首个信息/方案 | 🔴 高 |
| **可用性启发** (Availability Heuristic) | 最近/最新的例子主导判断 | 🟡 中 |
| **过度自信** (Overconfidence) | 未经验证的断言，高确定性表达 | 🔴 高 |
| **框架效应** (Framing Effect) | 问题表述方式影响判断方向 | 🟡 中 |
| **幸存者偏差** (Survivorship Bias) | 只关注成功案例，忽略失败案例 | 🟡 中 |
| **后见之明** (Hindsight Bias) | 事后认为结果"早就知道" | 🟢 低 |
| **基本归因错误** (Fundamental Attribution Error) | 高估内因、低估外因 | 🟡 中 |
| **沉没成本** (Sunk Cost Fallacy) | 因为已有投入而继续 | 🟡 中 |

#### 效率适配指标
- **过度分析检测**：对于简单任务进行过度推理（Overthinking Score）
- **草率判断检测**：对于复杂任务过早收敛（Premature Closure）
- **步骤经济性**：工具调用次数与任务复杂度的比率（Step Efficiency）

## 🔧 二、监控方法与工具

### 2.1 实时监控（Inline Monitoring）

在Agent执行过程中，对每个关键步骤进行"影子审计"：

```
Agent执行 → 思维监控层（shadow audit）→ 发出预警 / 记录
```

**监控节点**：
1. **任务启动**：记录初始假设、任务理解
2. **信息搜索后**：检查搜索策略、信息源多样性
3. **方案生成时**：检查方案空间探索范围
4. **决策点**：记录决策理由、备选方案
5. **执行后**：记录结果与预期的偏差

### 2.2 事后审计（Post-hoc Audit）

任务完成后，使用审计框架回溯整个思维过程：

```python
# 事后审计流程
audit_session(
    session_data="session.json",
    dimensions=["logical_rigor", "information_adequacy", "bias_control", "efficiency_fit"],
    depth="deep"  # "quick" | "standard" | "deep"
)
```

### 2.3 偏差检测工具箱

#### 确认偏差检测
```
检测规则：
1. Agent搜索时是否使用了对称搜索词（正反两面）？
2. Agent在找到支持性证据后是否主动寻找反例？
3. Agent总结时是否提及对立观点？
→ 任一为否 → 发出确认偏差预警
```

#### 锚定效应检测
```
检测规则：
1. Agent的第一个方案是否成为后续讨论的基准？
2. Agent是否明确考虑过至少2个替代方案？
3. 替代方案是否被真正评估（而非走过场）？
→ 1为是 + 2或3为否 → 锚定效应预警
```

#### 过度自信检测
```
检测规则：
1. Agent是否使用了绝对化表述（"一定""肯定""绝对"）？
2. Agent是否有证据支撑所有确定性断言？
3. Agent是否标注了不确定性区域？
→ 锚点计数 ≥ 2 且缺乏证据 → 过度自信预警
```

## 📊 三、评估框架

### 3.1 思维质量评分卡（Thinking Quality Scorecard）

每项任务完成后自动生成评分卡：

```
========== 思维质量评分卡 ==========
任务：<任务描述>
会话ID：<session_id>
评估时间：<timestamp>

📊 总分：XX/100（等级：S/A/B/C/D）

┌─────────────────────────────────┐
│ 维度            得分    权重    │
├─────────────────────────────────┤
│ 逻辑严谨性      XX/100  30%    │
│ 信息充分性      XX/100  25%    │
│ 偏差控制        XX/100  25%    │
│ 效率适配        XX/100  20%    │
├─────────────────────────────────┤
│ 加权总分        XX/100         │
└─────────────────────────────────┘

偏差检测结果：
  ✅ 无确认偏差
  ⚠️ 轻微锚定效应（首次方案权重过高）
  ✅ 无过度自信（不确定性标注充分）

关键发现：
  1. 决策点#3缺少备选方案分析
  2. 信息搜索仅使用1个来源，建议多源验证
  3. 推理链条完整，无跳跃

优化建议：
  → 在关键决策前，强制生成2+备选方案
  → 信息搜索时使用至少2个独立来源
  → 继续保持良好的不确定性标注习惯
=========================================
```

### 3.2 等级定义

| 等级 | 分数范围 | 含义 |
|------|----------|------|
| **S** | 90-100 | 卓越：推理严谨，信息充分，无偏差，效率高 |
| **A** | 80-89 | 优秀：少数小问题，整体质量高 |
| **B** | 70-79 | 良好：存在可改进空间，但不影响结果 |
| **C** | 60-69 | 一般：存在中等偏差或信息不足，可能影响结果 |
| **D** | <60 | 需要改进：存在严重偏差、逻辑错误或信息严重不足 |

### 3.3 偏差严重度处理策略

| 严重度 | 处理策略 |
|--------|----------|
| 🔴 高 | **阻断**：暂停执行，要求Agent自我纠正 |
| 🟡 中 | **预警**：发出警告，记录到评估报告 |
| 🟢 低 | **记录**：记录到评估报告，不干预执行 |

## 🔄 四、优化建议生成

### 4.1 自动优化建议

根据评分卡中的弱点，自动生成针对性建议：

```python
def generate_optimization_suggestions(scorecard):
    suggestions = []
    
    if scorecard.logical_rigor < 70:
        suggestions.append({
            "type": "logical_rigor",
            "suggestion": "在推理时使用「前提→推理→结论」结构，显式标注每一步",
            "practice": "在复杂推理前先列出核心假设"
        })
    
    if scorecard.information_adequacy < 70:
        suggestions.append({
            "type": "information",
            "suggestion": "关键决策前使用至少2个独立信息源进行三角验证",
            "practice": "在信息搜索后先问：'还有什么我不知道的？'"
        })
    
    if scorecard.bias_control < 70:
        suggestions.append({
            "type": "bias",
            "suggestion": f"检测到的偏差：{scorecard.detected_biases}",
            "practice": "对每个重要判断，主动思考反方观点（Steelman对手论证）"
        })
    
    if scorecard.efficiency_fit < 70:
        suggestions.append({
            "type": "efficiency",
            "suggestion": "根据任务复杂度调整分析深度，避免过度/不足分析",
            "practice": "在开始前评估任务复杂度（1-5级），匹配合适的分析深度"
        })
    
    return suggestions
```

### 4.2 思维模式优化

#### 模式1：红队思维（Red Teaming）
在做出重要决策前，主动扮演对手角度：
```
角色切换：如果我是一个挑剔的审核者...
问题：这个方案最薄弱的地方是什么？
条件：在什么条件下这个方案会失败？
```

#### 模式2：预检验证（Pre-mortem）
在执行前假设已经失败，反向追溯原因：
```
假设：项目已经失败
追溯：失败的根本原因是什么？
预防：现在可以做什么来防止？
```

#### 模式3：钢铁人论证（Steelmanning）
构建对手观点最强的版本：
```
当前观点：[Agent的结论]
对手观点最强的版本：[构建最佳反方论证]
比较：在对手观点最强的情况下，我的论证还成立吗？
```

### 4.3 与现有Skill集成

```
thinking-monitor ←→ reasoning-trace
    ├── 记录推理过程 → 思维监控分析
    ├── 偏差检测结果 → 更新skill修改建议
    └── 质量评分 → 关联到hermes-dojo自我进化

thinking-monitor ←→ process-thinking
    ├── 流程拆分后 → 对每个环节进行思维质量检查
    └── 工作流调试 → 使用偏差检测找根因

thinking-monitor ←→ hermes-dojo
    ├── 累积评分数据 → 追踪思维质量趋势
    └── 发现系统性问题 → 触发skill改进
```

## 🔧 五、实用工具和命令

### 5.1 快速思维检查（Quick Check）

在做决策前快速自检：

```
⚡ 思维快速检查 ⚡
1. 我有没有跳步？（逻辑链完整性）
2. 反方观点是什么？（偏差控制）
3. 我的信息够吗？（信息充分性）
4. 这个分析深度合适吗？（效率适配）
```

### 5.2 偏差自检清单

在得出重要结论前，逐一检查：

```
□ 我是否在寻找支持性证据而回避反面证据？（确认偏差）
□ 我是否过度依赖第一个想到的方案？（锚定效应）
□ 我是否把一些假设当成了确定事实？（过度自信）
□ 我是否只考虑了成功案例？（幸存者偏差）
□ 我是否被最近的信息过度影响？（可用性启发）
□ 这个问题换个方式问我还会得到同样的答案吗？（框架效应）
□ 我是否因为已经投入了努力而坚持当前方向？（沉没成本）
```

### 5.3 评估报告生成

```python
# 生成完整评估报告
from thinking_monitor import ThinkingMonitor

monitor = ThinkingMonitor()
monitor.load_session("session_data.json")
report = monitor.generate_report(format="markdown")  # "text" | "markdown" | "json"
print(report)
```

## 📝 六、使用场景

### 场景1：实时预警
```
Agent: 我确定问题出在配置文件，让我修改它
[思维监控检测到"确定"绝对化表述 + 缺少验证步骤]
⚠️ 过度置信预警：请在修改前先验证配置文件确实是问题根源
Agent: 好的，让我先读取配置文件和日志交叉验证...
```

### 场景2：任务复盘的思维审计
```
用户: 看看上次任务我的思维有什么问题
AI: [加载session数据]
AI: [运行思维审计]
AI: 发现3个问题：
  1. 确认偏差：搜索时只搜了"为什么A方案对"，没搜"A方案的局限"
  2. 锚定效应：第一个方案的权重占了决策的80%
  3. 信息不足：关键决策只用了1个信息来源
  建议：下次在关键决策前运行「偏差自检清单」
```

### 场景3：思维质量追踪
```
用户: 看看我最近的思维质量趋势
AI: [汇总最近10次会话的评分卡]
AI: 
  📈 思维质量趋势（最近10次会话）
  逻辑严谨性：72% → 78% → 85% ↗
  信息充分性：65% → 70% → 73% ↗
  偏差控制：80% → 82% → 80% →
  效率适配：75% → 68% → 72% ↘（注意：最近任务复杂度提升）
  总分：73 → 76 → 78 ↗
  
  🎯 持续改进方向：信息充分性（多源验证）
```

## 🚀 快速开始

任务完成后自动运行思维审计：

```
思维审计流程：
1. 确认任务完成
2. 自动运行思维监控检查
3. 生成评分卡
4. 如有严重问题，触发优化建议
5. 保存到 ~/.hermes/monitoring/ 目录
```

## 📚 相关资源

- **reasoning-trace skill**: 推理过程记录 → 思维监控的分析输入
- **process-thinking skill**: 流程分解 → 按环节监控思维
- **hermes-dojo skill**: 累积评分 → 自我进化
- **epistemology skill**: 认识论工具 → 知识类型与置信度校准
- **logic-check skill**: 逻辑检查 → 更深入的逻辑层面验证

## 📊 存储结构

```
~/.hermes/
├── monitoring/
│   ├── scorecards/              # 评分卡存档
│   │   ├── YYYY-MM-DD/
│   │   │   ├── session_XXX.json
│   │   │   └── ...
│   │   └── index.json
│   ├── trends/                  # 趋势分析
│   │   ├── weekly_report.json
│   │   └── monthly_report.json
│   └── config.yaml              # 监控配置（阈值、权重等）
```

## 🐍 代码实现

核心监控逻辑已实现在 `references/client.py`：
```python
# 使用方法
import sys
sys.path.insert(0, "~/.hermes/skills/hermes/thinking-monitor/references")
from client import ThinkingMonitor, quick_scan, analyze_session

monitor = ThinkingMonitor()
monitor.load_session("session.json")
report = monitor.generate_report("markdown")
print(report)
monitor.save_scorecard("task_001")
```

命令行使用：
```bash
python references/client.py session.json --format markdown
python references/client.py --quick-check
python scripts/check_thinking.py --bias-check
```

## ⚙️ 配置

可通过 `~/.hermes/monitoring/config.json` 配置：

- 维度权重调整
- 偏差检测灵敏度
- 预警阈值
- 自动/手动模式
- 报告格式偏好
