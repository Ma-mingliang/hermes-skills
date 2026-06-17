---
name: ai-daily-digest-verification
description: "AI日报验证系统 - 在推送前验证报告质量"
origin: custom
version: "2.0.0"
---

# AI日报验证系统

## When to Use

在生成报告后、推送前使用，验证报告是否符合skill要求。

## Verification Phases

### Phase 1: 结构验证
检查报告是否包含所有必需板块：
- [ ] 一、🤖 Agent生态
- [ ] 二、🛠️ Skills市场
- [ ] 三、📊 模型动态
- [ ] 四、📰 行业热点 + 🏭 行业应用
- [ ] 五、🔌 MCP动态
- [ ] 六、📊 数据面板
- [ ] 七、🔮 核心信号
- [ ] 八、📖 AI基础知识

### Phase 2: Agent生态验证
- [ ] Agent定义存在
- [ ] 📌使用指南（Claude Code/Gemini CLI/Codex）
- [ ] ⭐高星全能Agent表格（含Stars/痛点/优势/定价/GitHub）
- [ ] ⭐高星专精Agent表格（含领域/痛点/GitHub）
- [ ] 专精Agent有前辈对比文字分析（相似/不同/解决/原理）
- [ ] 🧩Agent组件表格（含解决什么Agent的问题）
- [ ] 每个Agent有GitHub链接

### Phase 3: Skills市场验证
- [ ] Skills定义存在
- [ ] 6类emoji全覆盖（📉🔒⚡🔬🔍📦）
- [ ] 第五类（🔍检测正常工作）包含验证/监控/审计类skill：verification-loop、skill-stocktake、canary-watch、cache-audit等
- [ ] 第六类（📦补充类/其他）包含资源索引集合：awesome-*系列、hermes-atlas、skill-scout等
- [ ] 每个Skill有痛点描述（按9种问题类型框架）
- [ ] 每个Skill有原理分析（🎯原理+🔧操作+📊效果+👤案例）
- [ ] 每个Skill有GitHub链接
- [ ] 每个Skill有前辈对比（表格+解决的问题）

### Phase 4: 痛点描述验证（9种问题类型框架）
检查每个Agent/Skill的痛点是否按框架描述：
- [ ] 能力缺失型：AI可以解决但没有好的使用方案
- [ ] 使用不便型：人使用AI时的不便之处
- [ ] 成本过高型：API/部署成本不可控
- [ ] 安全风险型：AI行为不可控
- [ ] 效率低下型：AI工作流程繁琐
- [ ] 知识壁垒型：不知道怎么用AI
- [ ] 协作困难型：多Agent/多人协作不便
- [ ] 数据孤岛型：Agent间数据不互通
- [ ] 行业落地型：AI技术难以落地到具体行业

### Phase 5: 模型动态验证
- [ ] 模型官网监控提及
- [ ] HN热点模型新闻（>=5条）
- [ ] OpenRouter数据
- [ ] 对比网站链接（openrouter.ai/lmarena.ai/artificialanalysis.ai）

### Phase 6: 行业应用验证
- [ ] 行业热点有链接
- [ ] 行业应用表格（>=3个行业）
- [ ] 36kr来源
- [ ] HN来源

### Phase 7: MCP动态验证
- [ ] MCP定义存在（"AI Agent的USB接口"）
- [ ] MCP监控标准应用正确（Stars>100新项目 / Stars>5000重大更新）
- [ ] MCP项目表（含Stars/功能/GitHub/分类归属）
- [ ] MCP七大分类全覆盖（🌐浏览器控制/💻代码智能/🗄️数据库/🔗工作流自动化/🔌API集成/🔒安全/🏗️开发框架）
- [ ] MCP评估维度完整（社区热度/功能完整度/集成便利性/安全风险/维护活跃度中至少3项）

### Phase 8: 数据面板验证
- [ ] 数据面板存在
- [ ] 区分今日/本周/历史
- [ ] 包含所有分类统计

### Phase 9: 核心信号验证
- [ ] 核心信号>=3条
- [ ] 信号有热度标注

### Phase 10: AI基础知识验证
- [ ] 今日目标
- [ ] 核心概念
- [ ] 为什么重要
- [ ] 常见误解
- [ ] 延伸阅读
- [ ] 小测验
- [ ] 主线标注

### Phase 11: 格式验证
- [ ] 用emoji编号（无"第X类"）
- [ ] 无板块标题重复
- [ ] GitHub链接>=15个
- [ ] 表格格式正确

### Phase 12: 数据来源透明度验证（2026-05-31新增）
- [ ] 报告末尾是否有数据来源汇总表
- [ ] 模型版本号是否有API/官网来源（无来源→删除或标注"未能获取"）
- [ ] 量化效果数据（"降低X%"、"提升X倍"）是否有来源链接（无来源→删除）
- [ ] 行业新闻是否有原文链接（无来源→删除）
- [ ] "基于知识"内容是否标注了⚠️
- [ ] 是否存在凭记忆编造的数据（如未经验证的版本号、效果百分比）

## Output Format

验证完成后输出：

```
AI日报验证报告
==============

Phase 1  结构验证:     [PASS/FAIL] (X/8板块)
Phase 2  Agent生态:    [PASS/FAIL] (X项)
Phase 3  Skills市场:   [PASS/FAIL] (X项)
Phase 4  痛点描述:     [PASS/FAIL] (X/9类型)
Phase 5  模型动态:     [PASS/FAIL] (X项)
Phase 6  行业应用:     [PASS/FAIL] (X项)
Phase 7  MCP动态:      [PASS/FAIL] (X项)
Phase 8  数据面板:     [PASS/FAIL] (X项)
Phase 9  核心信号:     [PASS/FAIL] (X条)
Phase 10 AI基础知识:   [PASS/FAIL] (X项)
Phase 11 格式验证:     [PASS/FAIL] (X项)

Overall:   [READY/NOT READY] for push

Issues to Fix:
1. ...
2. ...
```

## Fix Loop

如果验证失败：
1. 修复问题
2. 重新生成报告
3. 再次验证
4. 直到全部通过
