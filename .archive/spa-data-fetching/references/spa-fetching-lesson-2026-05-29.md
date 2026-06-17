# SPA获取教训：2026-05-29 实战案例

## 事件经过

1. 用户最初的日报写了 `Claude Opus 4.8`、`GPT-5.5`、`Gemini 3.1` —— **这些都正确**
2. 我用 `web_fetch` 抓取 artificialanalysis.ai → 拿到旧缓存数据（显示 Claude Opus 4、GPT-4.1）
3. 基于旧数据，我"纠正"了用户正确的版本号 → **灾难性错误**
4. 用户用手机截图证明了排行榜上确实有 Claude Opus 4.8 和 GPT-5.5
5. 最终结论：**我的"纠正"反而是错误的**

## 根因分析

```
web_fetch 抓取 SPA 站点
    → 拿到旧缓存/静态骨架（artificialanalysis.ai是React SPA）
    → 误以为"最新数据"
    → 错误"纠正"正确信息
    → 灾难
```

子任务的 browser 工具也没有真正执行页面渲染（返回的是知识库内容而非实时数据）。

## 重要澄清：模型版本号

子任务报告的模型版本号（Claude Opus 4.8、GPT-5.5、Gemini 3.1）**最终被用户截图证实为真实存在**。
但子任务的"正确"来自训练数据推测，而非实时API获取——是"对了但理由错了"。
这与hindsight GitHub仓库（纯编造）不同，但验证流程应相同：**所有子任务数据必须实时验证**。

## 正确做法

1. **SPA站点必须用主任务的browser工具**（不是子任务，不是web_fetch）
2. **browser失败时**：说"无法验证"，而不是用旧数据"纠正"
3. **用户截图 > 一切**：用户手机截图是最可靠的数据源
4. **vision_analyze可以读取截图**：用它从用户截图中提取排行榜数据

## 已知SPA站点（必须用browser）

| 站点 | 数据类型 | web_fetch结果 |
|------|---------|--------------|
| artificialanalysis.ai | 模型排名 | 旧缓存/空壳 |
| lmarena.ai | Chatbot Arena | 旧缓存/空壳 |
| openrouter.ai | 使用热度 | 旧缓存/空壳 |
| huggingface.co | 部分页面 | 部分可用 |
| GitHub API | REST API | ✅ 正常 |
| HN Algolia | REST API | ✅ 正常 |
