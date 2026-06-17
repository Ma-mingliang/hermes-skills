# 科研辅助Skills技术路线分析

> 2026-05-29 | GitHub主流科研Skills深度对比

## 三条技术路线

### 路线1：工作流编排（ARIS ⭐10,958）
- **仓库**: https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep
- **原理**: 80+个.md技能文件通过工作流串联，实现端到端科研自动化
- **核心创新**: 跨模型审查（Claude/GPT/Gemini交叉验证）、研究Wiki长期记忆、专利管线
- **覆盖领域**: ML/AI通用、CV、NLP、理论研究、通信/无线、架构/EDA、专利/法律、机器人
- **支持会议**: ICLR/NeurIPS/ICML/CVPR/ACL/AAAI/ACM/IEEE
- **关键技能**: arxiv, semantic-scholar, openalex, idea-discovery, paper-write, proof-writer, patent-pipeline
- **特点**: "方法论而非平台"，Markdown-only，跨Agent兼容

### 路线2：知识库（Orchestra Research ⭐9,054）
- **仓库**: https://github.com/Orchestra-Research/AI-Research-SKILLs
- **原理**: 98个细分技能覆盖AI研究全栈，23个类别
- **核心创新**: Agent-Native Research Artifact、GRPO训练、vLLM部署
- **覆盖范围**: Autoresearch/Ideation/Paper Writing/Model Architecture/Fine-Tuning/Post-Training/Distributed Training/Optimization/Inference/Evaluation/Safety/RAG/Multimodal/Mech Interp
- **特点**: 工程导向，不仅覆盖研究流程还包含大量工程实现技能

### 路线3：写作优化（Master-cai ⭐3,044）
- **仓库**: https://github.com/Master-cai/Research-Paper-Writing-Skills
- **原理**: 基于彭思达教授开放笔记，审稿人视角写作方法论
- **核心创新**: 对抗性自审、反向大纲检查逻辑漏洞、最小墨水表（Tufte原则）
- **写作工作流**: 澄清故事→章节指导→逐段重写→反向大纲→证据检查→对抗性自审
- **核心原则**: 一段一信息、首句即主题、名词自包含、句子间逻辑、视觉质量

## 其他重要项目

### ClaudePrism ⭐1,515
- **仓库**: https://github.com/delibae/claude-prism
- **路线**: 本地优先 + 桌面应用（Tauri 2 + Rust）
- **特点**: 离线LaTeX（Tectonic）、内置Python（uv+venv）、100+科学技能、数据隐私保护
- **对比OpenAI Prism**: 本地vs云端、Claude vs GPT、离线vs在线

### zLanqing Academic Skills ⭐199
- **仓库**: https://github.com/zLanqing/codex-claude-academic-skills
- **路线**: 中文优先 + 学术全流程
- **三大技能**: research-writing-skill（论文写作）、office-academic-skill（Word/PPT）、scientific-toolkit-skill（MATLAB/Python计算）
- **特点**: 针对中国科研工作者，三技能协作，OOXML级别编辑

## ARIS领域覆盖详情

| 领域 | 支持程度 | 核心技能 | 适用会议 |
|------|---------|---------|---------|
| ML/AI通用 | ⭐⭐⭐⭐⭐ | 全套80+技能 | ICLR/NeurIPS/ICML/CVPR/ACL |
| 计算机视觉 | ⭐⭐⭐⭐ | paper-figure/illustration | CVPR/ICCV/ECCV |
| 自然语言处理 | ⭐⭐⭐⭐ | paper-writing/comm-lit-review | ACL/EMNLP/NAACL |
| 理论研究 | ⭐⭐⭐⭐⭐ | proof-writer/proof-checker | NeurIPS/ICML/ICLR |
| 通信/无线 | ⭐⭐⭐⭐ | comm-lit-review | IEEE/ACM通信会议 |
| 计算机架构 | ⭐⭐⭐⭐ | dse-loop | MICRO/ISCA/HPCA |
| 专利/法律 | ⭐⭐⭐⭐⭐ | patent-pipeline全套 | 专利申请 |
| 生物医学 | ⭐⭐⭐ | 需社区扩展 | 生物信息学会议 |
| 机器人 | ⭐⭐⭐ | embodiment-description | ICRA/IROS/CoRL |
| 学术演讲 | ⭐⭐⭐⭐⭐ | paper-talk/slides/poster | 任何会议 |

## ARIS已安装状态

- 安装位置: `~/.hermes/skills/aris/`
- 有效skills: 77个（4个缺少SKILL.md：shared-references、skills-codex系列）
- 分类: 文献调研(8)、创意生成(3)、实验设计(6)、论文写作(6)、审稿回复(7)、可视化(7)、专利(6)、理论证明(2)、演讲(3)、工具(7)、研究流程(7)、其他(13)
- arXiv API有429限流问题，需等待重试

## 推荐组合

1. **ARIS + Master-cai**: 研究流程 + 写作质量
2. **Orchestra + zLanqing**: 工程技能 + 中文写作
3. **ClaudePrism独立使用**: 注重隐私的科学写作

## 未来趋势

1. 技能格式标准化（SKILL.md + references/）
2. 跨平台兼容（任意Agent方向发展）
3. 本地化增强（数据隐私成为重要考量）
4. 垂直深化（从通用科研向特定领域深化）
5. 协作增强（多Agent协作、跨模型验证成为标配）
