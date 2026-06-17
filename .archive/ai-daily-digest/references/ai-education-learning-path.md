# AI基础教育板块 - 热词驱动学习路径

## 核心设计原则

1. **热词驱动**：以AI热词为主线，每个热词都是一个"问题→解决方案"的完整故事
2. **问题→方案结构**：不能把问题和解决方案分开讲
3. **由浅入深**：先讲"是什么"，再讲"为什么"，最后讲"怎么做"
4. **类比优先**：用生活中的例子解释技术概念
5. **两条主线**：每个热词必须标注属于哪条主线

## 课程结构（两阶段）

### 第一阶段：AI发展历史（1950-2017）
按时间线讲清楚技术积累，重点讲人物故事和技术突破。

### 第二阶段：大模型时代（2017-2026）
按两条主线交替讲，包含交互模式。

详见 `ai-education-course-structure.md`

## 热词清单（按学习顺序）

```
第一阶段（1950-2017）：
感知机 → 反向传播 → CNN → RNN → SVM → LSTM → Attention → Transformer

第二阶段（2017-2026）：
LLM → Token → Parameters → Pre-training → BERT → GPT → 
Fine-tuning → RLHF → ChatGPT → Temperature → Prompt → 
Hallucination → Context Window → RAG → Embedding → Vector DB → 
Agent → Function Calling → MCP → Skills → Workflow → Dify/Coze → 
Vibe Coding → Context Engineering → CoT → Quantization → 
Multi-Agent → A2A → HITL → Guardrails → GraphRAG → Multimodal
```

## GitHub教程资源汇总

### LLM基础教程
- [mlabonne/llm-course](https://github.com/mlabonne/llm-course) - 79,697 stars - LLM入门课程
- [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) - 54,319 stars - 从零构建智能体

### Prompt Engineering教程
- [anthropics/prompt-eng-interactive-tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) - 36,008 stars - Anthropic官方Prompt教程
- [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering) - 7,545 stars - 22种Prompt技术

### RAG教程
- [patchy631/ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) - 35,353 stars - LLMs, RAGs and AI agent深度教程
- [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) - 27,608 stars - RAG高级技术

### 幻觉相关
- [vectara/hallucination-leaderboard](https://github.com/vectara/hallucination-leaderboard) - 3,266 stars - LLM幻觉排行榜
- [stanford-oval/WikiChat](https://github.com/stanford-oval/WikiChat) - 1,592 stars - 通过RAG减少幻觉

### Skills相关
- [mattpocock/skills](https://github.com/mattpocock/skills) - 109,570 stars - 工程师实用Skills
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) - 159,969 stars - 改进Claude Code行为的Skills
- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - 84,036 stars - UI/UX设计Skills
- [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) - 1,920 stars - Skills最佳实践

### Agent教程
- [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) - 22,248 stars - GenAI Agent教程
- [affaan-m/ECC](https://github.com/affaan-m/ECC) - 196,760 stars - Agent性能优化系统

### 工作流平台
- [langgenius/dify](https://github.com/langgenius/dify) - 142,980 stars - Dify开源平台
- [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) - 20,866 stars - Coze Studio
- [langchain-ai/langchain](https://github.com/langchain-ai/langchain) - 137,872 stars - LangChain
- [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) - 33,235 stars - LangGraph

### MCP相关
- [microsoft/mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners) - 16,213 stars - MCP入门
- [modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry) - 6,867 stars - MCP注册中心

### Token压缩
- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) - 65,733 stars - Token压缩
- [Context-Engine-AI/Context-Engine](https://github.com/Context-Engine-AI/Context-Engine) - 392 stars - 上下文压缩

### AI历史与Transformer
- [atfortes/Awesome-LLM-Reasoning](https://github.com/atfortes/Awesome-LLM-Reasoning) - 3,621 stars - LLM推理综述
- [AutoGPTQ/AutoGPTQ](https://github.com/AutoGPTQ/AutoGPTQ) - 5,062 stars - 模型量化

## 内容原则

1. **热词驱动**：以AI热词为主线，每个热词都是一个完整故事
2. **问题→方案**：先讲问题，再讲对应的多个解决方案
3. **由浅入深**：先讲"是什么"，再讲"为什么"，最后讲"怎么做"
4. **类比优先**：用生活中的例子解释技术概念
5. **循序渐进**：每天只讲一个核心概念，不贪多
6. **实践结合**：每周有实践环节，加深理解
7. **可追溯**：每天的内容有编号，方便回顾
8. **资源丰富**：每个主题都有GitHub教程链接
9. **两条主线**：每个热词必须标注属于哪条主线
