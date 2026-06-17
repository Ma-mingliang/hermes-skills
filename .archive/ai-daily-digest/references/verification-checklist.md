# AI日报验证流程

> 在生成报告后、推送前必须运行的验证系统

## 验证时机

```
数据收集 → 分类 → 报告生成 → [验证循环] → 推送
                                    ↑
                              修复问题后重新验证
```

## 11个Phase检查清单

### Phase 1: 结构验证 (8项)
- [ ] 一、🤖 Agent生态
- [ ] 二、🛠️ Skills市场
- [ ] 三、📊 模型动态
- [ ] 四、📰 行业热点
- [ ] 五、🔌 MCP动态
- [ ] 六、📊 数据面板
- [ ] 七、🔮 核心信号
- [ ] 八、📖 AI基础知识

### Phase 2: Agent生态 (7项)
- [ ] Agent定义
- [ ] 📌使用指南
- [ ] ⭐高星全能Agent表格
- [ ] ⭐高星专精Agent表格
- [ ] 专精Agent有前辈对比
- [ ] 🧩Agent组件
- [ ] GitHub链接>=10

### Phase 3: Skills市场 (9项)
- [ ] Skills定义
- [ ] 📉🔒⚡🔬🔍📦 6类emoji
- [ ] 痛点描述
- [ ] 原理分析
- [ ] GitHub链接

### Phase 4: 痛点描述 (9种问题类型)
- [ ] 能力缺失型
- [ ] 使用不便型
- [ ] 成本过高型
- [ ] 安全风险型
- [ ] 效率低下型
- [ ] 知识壁垒型
- [ ] 协作困难型
- [ ] 数据孤岛型
- [ ] 行业落地型

### Phase 5: 模型动态 (4项)
- [ ] 模型官网监控
- [ ] HN热点模型新闻>=5
- [ ] OpenRouter数据
- [ ] 对比网站链接

### Phase 6: 行业应用 (5项)
- [ ] 行业热点有链接
- [ ] 行业应用表格
- [ ] 行业覆盖>=3
- [ ] 36kr来源
- [ ] HN来源

### Phase 7: MCP动态 (10项)
- [ ] MCP定义
- [ ] MCP项目表
- [ ] 七大分类全覆盖

### Phase 8: 数据面板 (6项)
- [ ] 数据面板存在
- [ ] 今日/本周/历史区分
- [ ] 全能Agent统计
- [ ] 专精Agent统计

### Phase 9: 核心信号 (2项)
- [ ] 信号>=3条
- [ ] 有热度标注

### Phase 10: AI基础知识 (7项)
- [ ] 今日目标
- [ ] 核心概念
- [ ] 为什么重要
- [ ] 常见误解
- [ ] 延伸阅读
- [ ] 小测验
- [ ] 主线标注

### Phase 11: 格式验证 (4项)
- [ ] 用emoji编号（无"第X类"）
- [ ] 无板块标题重复
- [ ] GitHub链接>=15
- [ ] 表格格式正确

## 总检查项: 71项

## 验证输出格式

```
AI日报验证报告
==============
Phase 1  结构验证:     [PASS/FAIL] (X/8)
Phase 2  Agent生态:    [PASS/FAIL] (X/7)
Phase 3  Skills市场:   [PASS/FAIL] (X/9)
Phase 4  痛点描述:     [PASS/FAIL] (X/9)
Phase 5  模型动态:     [PASS/FAIL] (X/4)
Phase 6  行业应用:     [PASS/FAIL] (X/5)
Phase 7  MCP动态:      [PASS/FAIL] (X/10)
Phase 8  数据面板:     [PASS/FAIL] (X/6)
Phase 9  核心信号:     [PASS/FAIL] (X/2)
Phase 10 AI基础知识:   [PASS/FAIL] (X/7)
Phase 11 格式验证:     [PASS/FAIL] (X/4)

Overall:   [READY/NOT READY] for push
```
