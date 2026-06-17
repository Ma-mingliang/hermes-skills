# 科研辅助Skills深度分析（2026-05-29）

> 第四类Skills：科研辅助 — 论文写作、文献检索、数据分析、实验设计

## 三条技术路线

### 路线1：工作流编排（ARIS ⭐10,958）

**仓库**: https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep

**原理**：80+个.md技能文件通过工作流串联，实现端到端科研自动化。"方法论而非平台"——跨Claude Code/Codex/Cursor/OpenClaw等任意Agent。

**三阶段工作流**：
- 深度(Depth)：深入研究单一方向
- 广度(Breadth)：并行探索多方向（支持ultracode深度模式）
- 审查(Review)：跨模型交叉验证（Claude/GPT/Gemini）

**核心技能模块**：
| 类别 | 技能 | 功能 |
|------|------|------|
| 文献调研 | `arxiv`, `semantic-scholar`, `openalex`, `deepxiv` | 多源文献搜索 |
| 创意生成 | `idea-creator`, `idea-discovery-robot` | 研究想法发现 |
| 实验设计 | `experiment-plan`, `run-experiment` | 实验规划与执行 |
| 论文写作 | `paper-write`, `claims-drafting`, `formula-derivation` | 论文撰写 |
| 审稿回复 | `auto-review-loop`, `rebuttal` | 审稿意见处理 |
| 可视化 | `paper-figure`, `paper-poster` | 图表与海报 |
| 专利 | `patent-pipeline`, `prior-art-search` | 专利申请 |

**创新点**：
- 跨模型审查：不同LLM交叉验证结论
- 研究Wiki：`research-wiki`维护长期知识库
- HuggingFace #1 Paper of the Day（2026-05-29）

---

### 路线2：知识库（Orchestra Research ⭐9,054）

**仓库**: https://github.com/Orchestra-Research/AI-Research-SKILLs

**原理**：98个细分技能覆盖AI研究全栈，23个类别。独立.md文件，可单独使用或组合。

**技能分类（23类）**：
- Autoresearch(1) / Ideation(2) / ML Paper Writing(2)
- Model Architecture(5) / Fine-Tuning(4) / Post-Training(8)
- Distributed Training(6) / Optimization(6) / Inference(4)
- Data Processing(2) / Evaluation(3) / Safety & Alignment(4)
- RAG(5) / Multimodal(7) / Mech Interp(4)
- Agent-Native Research Artifact(3)

**创新点**：
- Agent-Native Research Artifact：为AI Agent设计的研究产物
- GRPO训练、vLLM部署等前沿工程技能
- npm包发布：`@orchestra-research/ai-research-skills`

---

### 路线3：写作方法论（Master-cai ⭐3,044）

**仓库**: https://github.com/Master-cai/Research-Paper-Writing-Skills

**原理**：基于彭思达教授开放学习笔记，将学术写作方法论转化为可执行AI技能。

**核心理念**：
- 审稿人视角：始终从审稿人角度审视论文
- 结构化写作：每个章节有明确修辞结构
- 证据驱动：每个claim必须有实验支持

**写作工作流**：
```
澄清论文故事 → 使用章节指导 → 逐段重写 → 反向大纲 → 证据检查 → 对抗性自审
```

**核心原则**：
1. 一段一信息：每段只传达一个核心观点
2. 首句即主题：第一句说明本段要说什么
3. 名词自包含：新术语使用前必须定义
4. 句子间逻辑：因果、对比、递进、举例
5. 视觉质量：图表是核心内容，不是装饰

**创新点**：
- 对抗性自审：模拟审稿人质疑视角
- 反向大纲：从已写内容反推结构，发现逻辑漏洞
- 最小墨水表：Tufte原则

---

### 路线4：本地优先（ClaudePrism ⭐1,515）

**仓库**: https://github.com/delibae/claude-prism

**原理**：Tauri 2 + Rust桌面应用，离线LaTeX + Python，100+科学技能。

**与OpenAI Prism对比**：
| 特性 | OpenAI Prism | ClaudePrism |
|------|-------------|-------------|
| AI模型 | GPT-5.2 | Claude Opus/Sonnet/Haiku |
| 运行时 | 浏览器（云端） | 原生桌面（Tauri 2 + Rust） |
| LaTeX | 云端编译 | Tectonic（嵌入式，离线） |
| Python | 无 | 内置uv + venv |
| 数据隐私 | 云端存储 | 本地存储 |

**创新点**：
- 离线优先：所有计算本地完成
- 一键Python环境：自动配置科学计算
- Zotero集成：文献管理与引用

---

### 路线5：中文优先（zLanqing ⭐199）

**仓库**: https://github.com/zLanqing/codex-claude-academic-skills

**原理**：三技能协作，专为中国科研工作者设计。

**三大技能模块**：
1. **research-writing-skill**：论文写作（中文优先，保留英文术语/公式）
2. **office-academic-skill**：学术Word/PPT（OOXML级别编辑）
3. **scientific-toolkit-skill**：科研计算（MATLAB/Python）

**协作工作流**：
```
论文写作：scientific-toolkit（数据出图）→ research-writing（写正文）→ office-academic（答辩PPT）
文献阅读：office-academic（PDF→Word报告）→ office-academic（组会PPT）
仿真研究：scientific-toolkit（仿真+配图）→ research-writing（方法+实验）
```

---

## 技术路线对比

| 维度 | ARIS | Orchestra | Master-cai | ClaudePrism | zLanqing |
|------|------|-----------|------------|-------------|----------|
| 核心理念 | 工作流编排 | 知识库 | 写作方法论 | 本地优先 | 中文优先 |
| 技能数量 | 80+ | 98 | 1 | 100+ | 3 |
| 覆盖范围 | 端到端研究 | AI研究全栈 | 论文写作 | 科学写作 | 学术全流程 |
| 技术栈 | Markdown-only | Markdown | Markdown | Tauri+Rust | Markdown |
| 平台兼容 | 任意Agent | 任意Agent | 任意Agent | 桌面应用 | Claude/Codex |

## 推荐组合

1. **ARIS + Master-cai**：研究流程 + 写作质量
2. **Orchestra + zLanqing**：工程技能 + 中文写作
3. **ClaudePrism独立使用**：注重隐私的科学写作

## 其他值得关注的科研Skills

| 仓库 | Stars | 定位 |
|------|-------|------|
| `andrehuang/research-companion` | 665 | 研究策略思维Agent |
| `xjtulyc/MedgeClaw` | 647 | 生物医学研究助手 |
| `lingzhi227/agent-research-skills` | 86 | 学术文献综述 |
| `ShZhao27208/Aut_Sci_Write` | 82 | 学术写作套件 |
| `jxtse/scientific-research-skills` | 42 | Zotero集成 |
| `neuromechanist/research-skills` | 28 | 基金写作 |
| `SNL-UCSB/paper-writing-skill` | 17 | 编辑原则 |
| `rpatrik96/research-agora` | 11 | 引用验证+实验复现 |
