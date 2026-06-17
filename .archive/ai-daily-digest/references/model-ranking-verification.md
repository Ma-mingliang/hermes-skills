# 模型排名获取与验证规则

> 2026-05-29 通过多次错误总结的规则

## 排名数据源

| 网站 | 类型 | 获取方式 | 可靠性 |
|------|------|---------|--------|
| artificialanalysis.ai | SPA | browser渲染 | ✅ 最权威 |
| lmarena.ai | SPA | browser渲染 | ✅ 用户投票 |
| openrouter.ai | SPA | browser渲染 | ✅ 使用热度 |

## 铁律

1. **SPA站点必须browser渲染** — web_fetch拿到的是旧缓存/静态骨架
2. **browser失败时** — 跳过排名板块，标注"今日未能获取"
3. **绝不用旧数据填充** — 用过时数据比没有数据更糟糕
4. **用户截图优先级最高** — 用户提供的手机截图 > browser > web_fetch
5. **不凭训练数据推测版本号** — 从4.0推测出4.8是错误的

## 教训：2026-05-29

- 我用web_fetch获取artificialanalysis.ai → 拿到旧数据（显示Claude Opus 4、GPT-4.1等老版本）
- 我基于旧数据"纠正"了用户正确的信息（Claude Opus 4.8、GPT-5.5确实存在）
- 用户用手机截图证明了我的"纠正"是错误的
- **本质问题：SPA网站需要完整JS渲染，web_fetch拿不到动态数据**

## 已验证的真实排名（2026-05-28截图）

| 排名 | 模型 | 分数 |
|------|------|------|
| 1 | Claude Opus 4.8 | 61 |
| 2 | GPT-5.5 | 60 |
| 3 | Gemini 3.1 Pro Preview | 57 |
| 4 | Qwen3.7 Max | 57 |
| 5 | Gemini 3.5 Flash | 55 |
| 6 | Kimi K2.6 | 54 |
| 7 | MiMo-V2.5-Pro | 54 |

**⚠️ 此排名仅供参考，每次日报必须重新获取**

## 模型监控三层体系

| 层级 | 网站 | 关注内容 |
|------|------|---------|
| 第一层：模型官网 | anthropic.com/openai.com/deepmind.google等 | 新发布/定价/Token Plan |
| 第二层：排名网站 | artificialanalysis.ai/lmarena.ai/openrouter.ai | 排名突涨/新上榜 |
| 第三层：调用网站 | openrouter.ai/together.ai | 价格变化/新模型上线 |
