---
name: bicycle-mbrl-research
description: "无人自行车Model-Based RL研究项目上下文。硬件平台：Arduino Nano ESP32 + 布瑞特FOC电机 + N100 IMU。当前任务：实车测试串级PID+LQR，然后系统辨识，再World Model建模。GitHub仓库 Ma-mingliang/bike。"
---

# 无人自行车MBRL研究项目

## 项目概述

**研究方向**: 基于深度强化学习的无人自行车控制（Model-Based）
**硬件平台**: Arduino Nano ESP32 + 布瑞特FOC电机 + N100 IMU
**项目位置**: E:\Code\bike
**研究方案**: E:\Code\bike\RESEARCH_PLAN.md

## 硬件架构

### 主控
- Arduino Nano ESP32 (双核240MHz, BLE 5.0)

### 执行器
- 布瑞特FOC电机 × 2 (CAN总线, 1Mbps)
  - 电机1 (ID=0x001): 驱动轮
  - 电机2 (ID=0x037): 平衡轮
- 舵机 × 2 (PWM控制, 50Hz)
  - servo1: 转向舵机
  - servo2: 辅助舵机

### 传感器
- N100九轴惯导模块 (UART, 115200bps)
  - 输出: pitch, roll, yaw, 加速度, 角速度

### 通信
- BLE NimBLE ("BikeESP32")
- 遥控: 微信小程序

## 研究方法论（重要！用户明确要求）

**铁律：先分析系统，再设计控制器。不能一开始就处于临界状态。**

正确流程：
1. 测量/获取系统物理参数（H, L, L₁, m, m_f, m_r, r_f, r_r）
2. 建立动力学模型（Carvallo-Whipple模型）
3. 线性化 + 状态空间表示
4. 可控性/可观性分析（可控性矩阵秩 = 状态维度）
5. 传递函数分析（极点、零点、稳定性）
6. 控制器设计（LQR/PID/RL）
7. 仿真验证 → 实车调试

参考：`references/thesis-analysis.md` 包含毕业论文中的完整动力学建模和LQR设计过程。

## 论文参考（重要！两篇论文，主次分明）

### 主参考：霍昱达终稿.pdf（74页，学士学位论文2026）
- 作者：霍昱达，导师：霍本岩副教授
- 题目：多模式无人自行车结构设计和控制方法
- **这是本项目的直接参考**，描述的就是本车的硬件和控制方法
- 详细分析见 `references/huoyuda-thesis-analysis.md`

### 次参考1：毕业论文.pdf（86页，硕士学位论文2025）
- 作者：龙宇，导师：霍本岩教授
- 题目：Research on Hierarchical Residual Reinforcement Learning Control Method for Unmanned Bicycles on Complex Terrain
- 核心方法：HRRL分层残差强化学习（LQR+TD3姿态控制，Stanley+RL路径跟踪）
- PDF编码问题：PyPDF2提取文本出现乱码，但英文摘要和公式可正常提取
- 详细分析见 `references/thesis-analysis.md`

### 次参考2：高佳旗-终稿.pdf（64页，本科毕业设计2025）
- 作者：高佳旗，导师：霍本岩副教授
- 题目：多自由度无人二轮车设计及实现
- 主控：STM32F103C8T6（与霍昱达的Arduino Nano ESP32不同）
- 重点贡献：电机系统辨识方法、两点法参数辨识、PWM-转速线性关系
- **注意**：这辆车的参数（H=0.2m, L=0.8m, m=20.3kg）与本项目差异很大，不可混用
- 详细分析见 `references/gaojiaqi-thesis-analysis.md`

**Pitfall：分析本车系统时，必须用霍昱达终稿.pdf，不是毕业论文.pdf或高佳旗终稿.pdf。**

## 当前控制能力（来自霍昱达终稿）

### Mode 1 (Segway模式/横向模式) - 串级PID控制
- 构型：两轮左右布置，轮轴共线，类似倒立摆
- 扶正机理：两侧轮毂电机差速产生俯仰扶正力矩
- 控制器：串级PID（速度外环 + 直立内环）
  - 速度外环：PI控制，输出目标俯仰角补偿量
  - 直立内环：PD控制，输出电机电流命令
- 输出：电流控制（±10mA步长）
- 频率：100Hz（10ms周期）
- 实验结果：稳态俯仰角标准差约0.16°，约88%采样点在±0.5°带内

### Mode 2 (Bike模式/纵向模式) - LQR控制
- 构型：前后轮纵向排列，自行车构型
- 扶正机理：前轮转向产生侧向加速度，形成扶正力矩
- 控制器：离散LQR（三阶状态反馈）
- 状态变量：x = [φ, φ̇, δ]ᵀ（侧倾角、侧倾角速度、前轮实际转角）
- 输入：u = δc（舵机命令角）
- LQR增益：K = [-5.313, -1.352, 0.379]
- 控制律：δc = -K·x = 5.313φ + 1.352φ̇ - 0.379δ
- 输出：舵机角度（PWM控制）
- 频率：50Hz（20ms周期，匹配舵机PWM周期）
- 安全限制：侧倾角±15°，侧倾角速度±120°/s
- 实验结果：95.7%侧倾角样本在±1°带内，全程在±2°带内

## 代码级实现状态（2026-05-30实际代码分析）

**重要原则：用户要求"从代码中真正找到项目的情况"，不要假设论文中的设计都已实现。**

### mode1.cpp - 横向模式实际实现
- **已实现串级PID控制（2026-05-30）**：速度外环 + 直立内环
- 速度外环：PI控制，输出目标俯仰角补偿量
  - 参数：SPEED_KP(3), SPEED_KI(4), SPEED_MAX_INTEGRAL(15), SPEED_FILTER_ALPHA(6), SPEED_TARGET(16)
  - 默认值：KP=0.5, KI=0.01, 积分限幅=5°, 滤波系数=0.1
- 直立内环：PD控制，输出电机电流命令
- 控制律：`targetAngle = mechanicalBase + mechTrim + speedOutput`
- 已移除：大角度Recover状态机、大角度保护
- 输出：双电机相同电流命令（不做差速转向）
- 实现细节见 `references/cascade-pid-implementation.md`

### mode2.cpp - 纵向模式实际实现
- LQR控制器，只计算舵机角，不直接控制电机
- LQR增益（代码中）：K0=-5.41460049, K1=-1.37771131, K2=0.38658890
- 舵机中位：85°，范围40°-130°，每帧最大步进1°
- 舵机一阶估计器：`deltaEstRad += (Ts/tau) * (deltaCmdRad - deltaEstRad)`
- 安全限制：俯仰角±15°，角速度±120°/s

### main.cpp - Bike模式时序
- 进入Bike模式后先等待10秒（舵机中立位）
- 然后运行LQR 5秒安全窗口
- 电机1以固定ERPM=1895运行，电机2失能
- 超过安全限制时停止电机，累计安全运行时间

### 实际状态 vs 论文设计的差距（2026-05-30更新）
| 功能 | 论文设计 | 代码实现 |
|------|---------|---------|
| 横向速度环 | 串级PID（速度外环+直立内环）| **已实现**（2026-05-30添加） |
| 横向大角度保护 | 有Recover状态机 | **已移除** |
| 纵向LQR | 完整三阶状态反馈 | **已实现**（只算舵机角）|
| 纵向电机控制 | 速度闭环 | **固定ERPM开环** |

### PID参数索引表（RobotContext.h，2026-05-30更新）
| 索引 | 名称 | 说明 |
|------|------|------|
| 0 | BALANCE_KP | 直立环比例系数 |
| 1 | BALANCE_KD | 直立环微分系数 |
| 2 | MECHANICAL_ANGLE | 工作点调整值（度） |
| 3 | SPEED_KP | 速度环比例系数 |
| 4 | SPEED_KI | 速度环积分系数 |
| 5 | SPEED_I_LIMIT | 速度环积分限幅 |
| 6 | SPEED_FILTER_ALPHA | 速度滤波系数 |
| 7 | TURN_KP | 转向环比例系数 |
| 8 | MAX_OUTPUT_ERPM | 输出ERPM限幅 |
| 9 | MAX_TARGET_SPEED | 油门最大目标速度 |
| 10 | MAX_TARGET_YAW_RATE | 转向最大偏航角速度 |
| 11 | PITCH_SAFE_LIMIT | 俯仰角安全阈值 |
| 12 | MAX_OUTPUT_CURRENT | 输出电流限幅（10mA） |
| 13 | START_CURRENT | 最小启动电流（10mA） |
| 14 | CURRENT_DEADBAND | 电流死区阈值（10mA） |
| 15 | SPEED_MAX_INTEGRAL | 速度环积分限幅（度）**新增** |
| 16 | SPEED_TARGET | 目标速度（ERPM）**新增** |

## 研究路径

### 第零阶段：系统分析（用户要求，应最先完成）
- [x] 收集物理参数（从霍昱达终稿.pdf获取）
- [x] 建立动力学模型
  - 横向模式：单自由度倒立摆模型（二阶）
  - 纵向模式：侧倾-转向耦合模型（三阶）
- [x] 线性化 + 状态空间表示
- [x] 可控性分析（两模式均完全可控）
- [x] 传递函数分析（极点位置、稳定性）
- [ ] 确定RL控制器参数的理论依据

### 第一阶段：基础功能测试与修复（当前任务，详细计划见 docs/detailed_plan.md）
- [ ] 1.1 硬件检查（IMU/CAN/PWM/BLE/电源）
- [x] 1.2 横向模式：添加速度外环（2026-05-30已实现，待烧录测试）
- [ ] 1.3 纵向模式：验证LQR平衡效果
- [ ] 1.4 问题修复与验证

### 第二阶段：系统辨识 + 数据采集（2-3周）
- **先做电机辨识**：阶跃PWM → 转速响应 → 辨识一阶惯性环节 K/(τs+1)
  - 方法：两点法（参考高佳旗论文）
  - 验证：检查时间常数和增益的合理性
- **横向模式辨识**：阶跃电流 → 俯仰角响应 → 辨识倒立摆参数
- **纵向模式辨识**：阶跃转向角 → 侧倾角响应 → 辨识自行车模型参数
- 数据记录：CSV格式，100Hz采样，包含所有状态变量和控制输入
- 详见 `references/gaojiaqi-thesis-analysis.md` 中的系统辨识实验方案

### 第三阶段：World Model建模（3-4周）
- 神经网络动力学模型
- 物理先验集成（利用LQR线性化模型）
- 不确定性估计（集成模型）

### 第四阶段：RL策略学习（4-6周）
- Model-Free: PPO/SAC用于平衡控制、转向控制
- Model-Based: TD-MPC2用于轨迹规划、避障
- 混合架构：高层Model-Based规划 + 低层Model-Free执行

### 第五阶段：创新点实现（4-6周）
1. Adaptive LQR-RL Hybrid
2. Data-Efficient World Model with Physics Priors
3. Sim-to-Real with System Identification
4. Safe Online Learning with CBF
5. Multi-Modal Fusion with Attention

### 第六阶段：论文撰写（2-4周）
- 目标会议: ICRA 2027 / IROS 2027

## 关键源代码文件

- `E:\Code\bike\bike\src\main.cpp` - 主调度模块
- `E:\Code\bike\bike\src\BriterDriver\BriterDriver.cpp` - CAN电机驱动
- `E:\Code\bike\bike\src\N100\N100.cpp` - IMU/AHRS驱动
- `E:\Code\bike\bike\src\mode1\mode1.cpp` - Segway平衡控制
- `E:\Code\bike\bike\src\mode2\mode2.cpp` - Bike LQR控制
- `E:\Code\bike\bike\src\RobotLink\RobotLink.cpp` - BLE通信

## 状态空间 (12维)

```python
s = [
    pitch, pitch_rate,      # 俯仰角 (N100 IMU)
    roll, roll_rate,        # 横滚角 (N100 IMU)
    yaw, yaw_rate,          # 航向角 (N100 IMU)
    steer_angle, steer_rate,# 转向角 (舵机反馈)
    motor1_speed, motor2_speed,  # 电机转速 (CAN反馈)
    linear_speed,           # 线速度 (估计)
    target_heading          # 目标航向 (BLE指令)
]
```

## 动作空间 (4维)

```python
a = [
    servo1_cmd,      # 转向舵机 (PWM: 500-2500μs)
    servo2_cmd,      # 辅助舵机 (PWM: 500-2500μs)
    motor1_speed,    # 电机1速度 (eRPM)
    motor2_speed     # 电机2速度 (eRPM)
]
```

## 微信讨论要点

1. 调参过程中的问题
2. 实车数据分享
3. 3D模型和质量参数
4. 创新点讨论
5. 进展同步

## 相关文件

- **主参考论文**: `E:\Code\bike\霍昱达终稿.pdf`（74页，学士论文2026，本项目直接参考）
- 次参考论文1: `E:\Code\bike\毕业论文.pdf`（86页，硕士论文2025，HRRL方法）
- 次参考论文2: `E:\Code\bike\高佳旗-终稿.pdf`（64页，本科毕设2025，系统辨识方法）
- 详细计划书（已推送GitHub）: `E:\Code\bike\docs\detailed_plan.md`
- GitHub仓库: https://github.com/Ma-mingliang/bike
- 研究方案: `E:\Code\bike\RESEARCH_PLAN.md`
- 3D模型: `E:\Code\bike\bike_L3\bike_SW建模\`
- PyBullet仿真: `E:\Code\bike\bike_L3\pybullet仿真\`
- 数据日志: `E:\Code\bike\bike\bike_observer_logs\`
- 微信小程序数据记录功能说明: `references/wx-data-recording.md`
- 信号流向图: `E:\Code\bike\信号流向图.pdf`
- 电源流向图: `E:\Code\bike\电源流向图.pdf`
- 总流程图: `E:\Code\bike\总流程图.pdf`
- 横向框图: `E:\Code\bike\横向框图.pdf`
- 布瑞特驱动器手册: `E:\Code\bike\布瑞特驱动器CAN编程手册（6.11固件版本）.pdf`
- N100惯导手册: `E:\Code\bike\WHEELTEC N100惯导模块通信接口与数据读取说明_2024.08.26.pdf`

## Pitfalls

1. **两篇论文不要搞混**：项目文件夹中有三篇论文：
   - 霍昱达终稿.pdf = 本项目的直接参考（学士论文2026，描述的就是这辆车）
   - 毕业论文.pdf = 上级项目参考（硕士论文2025，HRRL方法）
   - 高佳旗终稿.pdf = 前期项目参考（本科毕设2025，系统辨识方法）
   分析本车系统时必须用霍昱达终稿.pdf。

2. **毕业论文PDF编码问题**：PyPDF2提取文本出现乱码（扫描版或特殊编码）。但第6页起的英文摘要和第22-28页的公式/表格可正常提取。关键公式和参数见 `references/thesis-analysis.md`。

3. **模式名称对应关系**：
   - 横向模式 = Segway模式 = 两轮左右布置 = 倒立摆类系统 = 串级PID控制
   - 纵向模式 = Bike模式 = 前后轮排列 = 自行车构型 = LQR控制
   不要搞混！

4. **状态空间维度差异**：论文的LQR是3维（φ, φ̇, δ），仅用于Bike模式的平衡控制。我们的实际系统有12维状态。论文的模型是简化版，不能直接套用。

5. **系统分析顺序**：用户明确要求先做可控性分析再设计控制器。不要跳过系统分析直接调参。

6. **速度依赖性**：纵向模式的扶正能力与车速平方成正比（b = mhv²/JL），v=0时不可控。LQR必须在车辆具备前进速度时启用。

7. **LQR增益符号问题（重要！）**：论文中给出的LQR增益 K = [-5.313, -1.352, 0.379]，控制律 δc = -K·x。但计算连续闭环极点时发现有一个正实部极点（不稳定）。而使用相反符号 K = [5.313, 1.352, -0.379] 时所有闭环极点均为负实部（稳定）。可能原因：
   - 论文使用离散LQR（T_s=0.02s），增益针对离散系统设计
   - 增益符号约定可能与状态变量定义有关
   - **实际调试时必须验证闭环稳定性，不能盲目套用论文增益**

8. **不同论文的参数不能混用**：霍昱达的车（m=23.3kg, H=0.63m, L=1.17m）与高佳旗的车（m=20.3kg, H=0.2m, L=0.8m）参数差异很大。系统辨识必须基于本车实际参数。

9. **Windows环境下的文件操作**：此主机WSL不可用，terminal命令会报错。使用execute_code进行文件读写操作（import os + open/write），不要依赖terminal的cat/echo等命令。

10. **Git推送注意事项**：项目使用HTTPS方式推送到GitHub（https://github.com/Ma-mingliang/bike.git）。bike/tools/目录下有嵌套.git会导致git add失败，需要排除。推送时只添加必要的文件（docs/, bike/src/等），避免添加大型PDF和二进制文件。
