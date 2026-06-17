# Execution Log: 2026-05-28 (Session 2 - Major Corrections)

## User Feedback Summary

### Critical Corrections

1. **Agent分类结构** — 用户要求Agent必须分为两大类：
   - 全能型Agent（3个子类：使用指南、新出现、高星）
   - 专精型Agent（3个子类：使用指南、新出现、高星）
   
2. **对比、拆分、归纳** — 新出现的Agent必须执行这三步：
   - 对比：与已知Agent对比
   - 拆分：功能拆分、技术拆分、用户体验拆分
   - 归纳：选择建议、趋势观察

3. **100个网站的定义** — GitHub算1个网站，不同项目不是不同网站
   - 英文源：40个
   - 中文源：40个
   - GitHub：1个
   - API源：15个
   - 视频平台：抖音、B站、YouTube

4. **Skills定义** — Skills = .md文档，直接约束agent行为的指令文件
   - ✅ 真正的Skills：caveman、planning-with-files、context-engine
   - ❌ 不是Skills：Claude Code指南、awesome-gpt-prompt、Prompt-Forge

5. **Skills必须6类** — 不是5类，是6类：
   - (1)减少token消耗 (2)约束agent行为 (3)增加功能
   - (4)科研辅助 (5)检测正常工作 (6)补充类/其他

6. **链接必须GitHub** — 不能只有HN Algolia链接，必须附上GitHub链接

7. **不要新闻式内容** — 不要推送"创始人30天花费130万美元Token"这种内容

8. **视频平台热词** — 必须搜索抖音、B站、YouTube的AI相关热词

9. **每日对比机制** — 第二天与第一天对比，重复项标注为热点

### User Preferences

- 用户偏好结构化输出，包含表格、拆分分析、归纳总结
- 用户需要具体案例（"有人用它干出来了什么事情"）
- 用户可能对感兴趣的skills进行提问，需要提供详细信息
- 用户要求对比分析，不是简单的列表

### Technical Issues

1. **微信频率限制** — 短时间内多次推送会触发限制（ret=-2）
2. **DuckDuckGo超时** — 需要降级到HN Algolia API
3. **配置文件不存在** — 需要使用默认API源
4. **Reddit被封锁** — 无法访问

### Output Format

**消息1：全能型Agent**
- 使用指南、新出现（对比拆分归纳）、高星（多维度对比拆分归纳）

**消息2：专精型Agent**
- 使用指南、新出现（对比拆分归纳）、高星（多维度对比拆分归纳）

**消息3：Skills市场**
- 6类Skills，每类包含原理、操作、效果

**消息4：模型+行业+数据面板**
- 模型动态、行业应用、今日数据面板

### Key Learnings

1. **用户需求必须严格遵守** — 用户提供的结构化要求必须完全按照执行
2. **对比分析是核心** — 用户需要清晰的对比和选择建议
3. **Skills定义必须明确** — .md文档 vs 学习资源
4. **100个网站是域名数** — 不是项目数
5. **视频平台热词必须搜索** — 抖音、B站、YouTube
6. **每日对比机制** — 识别热点
