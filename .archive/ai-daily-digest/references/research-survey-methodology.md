# 科研调研方法论（Research Survey Methodology）

> 2026-05-29 | 基于ARIS工作流的领域调研全流程

## 五步调研框架

### Step 1: 文献调研（Literature Survey）

**搜索策略**：
- arXiv API: `http://export.arxiv.org/api/query?search_query=QUERY&max_results=10`
- Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/search?query=QUERY&limit=10`
- GitHub: `https://api.github.com/search/repositories?q=QUERY&sort=stars`

**关键词组合**：
- 核心方法 + 应用领域（如 "reinforcement learning bicycle control"）
- 变体搜索（如 "model-based RL", "MBRL", "world model"）
- 相关领域（如 "legged locomotion", "balance control"）

**⚠️ arXiv API限流**：
- arXiv API有严格的429限流（每3秒最多1次请求）
- 失败后等待5-10秒重试
- 备选：Semantic Scholar API（更宽松但也有429）
- 最可靠：直接web搜索获取论文信息

### Step 2: 方法分类与对比（Method Classification）

**分类维度**：
1. **技术路线**：Model-Free vs Model-Based vs Hybrid
2. **学习方式**：在线 vs 离线 vs 迁移
3. **模型类型**：确定性 vs 随机性 vs 集成
4. **规划方式**：无规划 vs MPC vs 树搜索

**对比表模板**：

| 方法 | 代表算法 | 优点 | 缺点 | 适用场景 |
|------|---------|------|------|---------|
| Model-Free | PPO/SAC | 简单 | 样本效率低 | 仿真环境 |
| Model-Based | TD-MPC/Dreamer | 样本效率高 | 模型误差 | 真实系统 |
| Hybrid | MBPO | 平衡 | 复杂 | 通用 |

### Step 3: 研究空白识别（Gap Analysis）

**常见空白类型**：
1. **领域空白**：某方法未应用于特定领域
2. **技术空白**：某技术问题未被解决
3. **评估空白**：缺乏标准化benchmark
4. **应用空白**：理论到实践的差距

**空白识别方法**：
- 搜索"survey" + 领域名，查看已有综述的"future work"
- 搜索近1年顶会论文，看"limitation"部分
- 搜索GitHub issues，看用户未解决的需求

### Step 4: 创新机会挖掘（Innovation Opportunities）

**创新模式**：
1. **跨领域迁移**：将A领域的方法应用到B领域
2. **技术组合**：结合两种已有方法的优点
3. **问题驱动**：从实际问题出发设计新方法
4. **理论突破**：发现新的理论洞见

**评估标准**：
- 新颖性：是否有人做过？
- 可行性：技术上是否可实现？
- 影响力：能解决多大的问题？
- 可发表性：适合什么级别的会议/期刊？

### Step 5: 技术路线规划（Technical Roadmap）

**规划模板**：

```
Phase 1: 基础搭建（1-2月）
├── 仿真环境搭建
├── Baseline实现
└── 数据收集

Phase 2: 核心创新（2-3月）
├── 方法设计
├── 算法实现
└── 初步验证

Phase 3: 实验验证（1-2月）
├── 基准对比
├── 消融实验
└── 鲁棒性测试

Phase 4: 论文撰写（1月）
├── 整理结果
├── 撰写论文
└── 准备投稿
```

## 硬件项目驱动的研究设计（Hardware-Driven Research Design）

> 当用户有实际硬件项目时，研究方案必须基于真实硬件参数，而非通用假设。

### 工作流

```
1. 读取硬件源代码 → 提取传感器/执行器/控制器参数
2. 分析现有控制方法 → 反推动力学模型
3. 设计RL研究 → 基于实际状态/动作空间
4. 写入研究方案 → 包含硬件特定参数
```

### 关键步骤

**Step 1: 硬件参数提取**
- 从 `main.cpp` 或配置文件中提取：
  - 传感器类型、频率、精度
  - 执行器类型、通信协议、控制范围
  - 现有控制器参数（如LQR的K矩阵）
  - 安全限制（角度、速度、扭矩）

**Step 2: 现有控制分析**
- 从控制器代码反推线性化模型
- 识别现有方法的局限性
- 找到可改进的空间

**Step 3: RL方案设计**
- 状态空间 = 传感器可用数据
- 动作空间 = 执行器控制命令
- 奖励函数 = 现有控制目标 + 新增优化目标
- 安全约束 = 现有安全限制的CBF形式化

**Step 4: 与现有系统集成**
- 设计模式切换机制（继承现有模式）
- 设计数据采集模块（收集训练数据）
- 设计部署方案（在现有MCU上运行推理）

### 示例：自行车MBRL研究

**硬件参数**（从源代码提取）：
- 主控: Arduino Nano ESP32 (双核240MHz)
- 电机: 布瑞特FOC × 2 (CAN总线, 1Mbps)
- 舵机: × 2 (PWM, 50Hz)
- IMU: N100九轴 (UART, 115200bps)
- 现有控制: Mode1 PD(Kp=59) + Mode2 LQR(K0=-5.41, K1=-1.38, K2=0.39)
- 安全限制: pitch ±15°, pitch_rate ±120°/s

**研究方案**（基于硬件）：
- 状态空间: 12维 (pitch, pitch_rate, roll, roll_rate, yaw, yaw_rate, steer_angle, steer_rate, motor1_speed, motor2_speed, linear_speed, target_heading)
- 动作空间: 4维 (servo1_cmd, servo2_cmd, motor1_speed, motor2_speed)
- 创新点: Physics-Informed (从LQR反推线性模型+NN残差), Multi-Modal (继承Segway/Bike模式), CBF (利用现有安全限制)

### 搜索结果
- arXiv: 429限流（需重试）
- Semantic Scholar: 429限流
- 基于知识库提供完整调研

### 方法分类
| 方法 | 代表 | 样本效率 | 安全性 | 泛化性 |
|------|------|---------|--------|--------|
| Model-Free | PPO/SAC | 低 | 差 | 中 |
| Model-Based | TD-MPC | 高 | 好 | 好 |
| Physics-Informed | PINN+RL | 最高 | 最好 | 最好 |

### 研究空白
1. 缺乏针对自行车的MBRL研究
2. Sim-to-Real gap未解决
3. 低速平衡控制挑战
4. 多模态感知融合
5. 安全约束下的在线学习

### 创新方向
1. Physics-Informed Neural Dynamics
2. Adaptive Model Ensemble
3. Hierarchical MBRL
4. Safe Exploration with CBF

## ARIS Skills在调研中的应用

| 调研阶段 | ARIS Skills | 功能 |
|---------|-------------|------|
| 文献搜索 | arxiv, semantic-scholar, openalex | 多源文献检索 |
| 创意生成 | idea-discovery, idea-creator | 研究方向发现 |
| 新颖性检查 | novelty-check, prior-art-search | 验证创新性 |
| 方法评估 | research-review | 专家级评审 |
| 实验规划 | experiment-plan, ablation-planner | 实验设计 |
| 论文写作 | paper-write, claims-drafting | 论文撰写 |
| 审稿回复 | rebuttal, auto-review-loop | 审稿处理 |
