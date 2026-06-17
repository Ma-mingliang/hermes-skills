# GitHub Academic/Research Skills Landscape

> 分析时间：2026-05-29 | 基于GitHub API深度调研

## 三条技术路线

GitHub上科研辅助Skills主要有三条路线：

### 路线1: 工作流编排（代表：ARIS ⭐10,958）
- **仓库**: wanshuiyin/Auto-claude-code-research-in-sleep
- **理念**: "方法论而非平台"，80+个.md技能文件协作
- **特点**: 轻量级Markdown-only，跨平台兼容（Claude Code/Codex/Cursor/OpenClaw）
- **三阶段工作流**: 深度(Depth) → 广度(Breadth) → 审查(Review)
- **核心技能分类**:
  - 文献调研: arxiv, semantic-scholar, openalex, deepxiv, alphaxiv
  - 创意生成: idea-creator, idea-discovery, idea-discovery-robot
  - 实验设计: experiment-plan, experiment-queue, run-experiment
  - 论文写作: paper-write, paper-writing, paper-plan, claims-drafting
  - 审稿回复: auto-review-loop, rebuttal, paper-claim-audit, kill-argument
  - 可视化: paper-figure, paper-illustration, mermaid-diagram
  - 专利: patent-pipeline, patent-novelty-check, prior-art-search
  - 理论证明: proof-writer, proof-checker（三种状态：PROVABLE/WEAKENING/NOT JUSTIFIED）
  - 演讲: paper-talk, paper-slides, slides-polish
- **创新点**: 跨模型审查（Claude/GPT/Gemini交叉验证），研究Wiki长期记忆，专利管线

### 路线2: 知识库（代表：Orchestra Research ⭐9,054）
- **仓库**: Orchestra-Research/AI-Research-SKILLs
- **理念**: 全栈AI研究技能库，98个细分技能覆盖23个类别
- **特点**: 工程导向，覆盖从Ideation到Deployment
- **类别**: Autoresearch/Ideation/ML Paper Writing/Model Architecture/Fine-Tuning/Post-Training/Distributed Training/Optimization/Inference/Tokenization/Data Processing/Evaluation/Safety & Alignment/Agents/RAG/Multimodal/Prompt Engineering/MLOps/Observability/Infrastructure/Mech Interp/Emerging Techniques/Agent-Native Research Artifact

### 路线3: 写作优化（代表：Master-cai ⭐3,044）
- **仓库**: Master-cai/Research-Paper-Writing-Skills
- **理念**: 基于彭思达教授开放学习笔记，审稿人视角写作
- **核心原则**: 一段一信息、首句即主题、名词自包含、句子间逻辑、对抗性自审
- **关键方法**: 反向大纲（从已写内容反推结构）、最小墨水表（Tufte原则）

## 其他值得关注的项目

| 项目 | Stars | 特点 |
|------|-------|------|
| ClaudePrism | 1,515 | 本地优先桌面应用，Tauri 2+Rust，离线LaTeX+Python，100+科学技能 |
| zLanqing/codex-claude-academic-skills | 199 | 中文优先，三技能协作（写作+Office文档+科研计算）|
| andrehuang/research-companion | 665 | 战略研究思维agent |
| xjtulyc/MedgeClaw | 647 | 生物医学AI研究助手 |
| lingzhi227/agent-research-skills | 86 | 深度学术文献综述 |
| ShZhao27208/Aut_Sci_Write | 82 | arXiv+PubMed+WoS文献搜索 |
| jxtse/scientific-research-skills | 42 | Zotero集成 |
| neuromechanist/research-skills | 28 | 基金撰写辅助 |

## 推荐组合

1. **端到端ML研究**: ARIS（最完整的科研工作流）
2. **AI工程实践**: Orchestra Research（98个细分技能）
3. **论文写作优化**: Master-cai（审稿人视角）
4. **科学写作+隐私**: ClaudePrism（本地优先，离线LaTeX）
5. **中文学术写作**: zLanqing（中文优先，三技能协作）

## 领域覆盖能力

| 领域 | ARIS支持 | 专用技能 |
|------|---------|---------|
| ML/AI通用 | ⭐⭐⭐⭐⭐ | 全套80+技能 |
| 计算机视觉 | ⭐⭐⭐⭐ | paper-figure/illustration |
| 自然语言处理 | ⭐⭐⭐⭐ | paper-writing/comm-lit-review |
| 理论研究 | ⭐⭐⭐⭐⭐ | proof-writer/proof-checker |
| 通信/无线 | ⭐⭐⭐⭐ | comm-lit-review |
| 计算机架构 | ⭐⭐⭐⭐ | dse-loop |
| 专利/法律 | ⭐⭐⭐⭐⭐ | patent-pipeline全套 |
| 生物医学 | ⭐⭐⭐ | 需社区扩展 |

## 关键发现

- 技能格式趋向统一：SKILL.md + references/ 目录结构
- 所有技能都在向"任意Agent"方向发展（跨平台兼容）
- 本地优先（数据隐私）成为重要趋势
- 从通用科研向特定领域深化是下一个方向
