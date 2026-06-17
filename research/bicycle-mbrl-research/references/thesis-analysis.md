# 毕业论文分析：复杂地形无人自行车分层残差强化学习控制

来源：E:\Code\bike\毕业论文.pdf（86页，郑州大学硕士论文，2025年5月）
作者：于龙，导师：霍本岩
英文标题：Research on Hierarchical Residual Reinforcement Learning Control Method for Unmanned Bicycles on Complex Terrain

## 核心方法

HRRL（Hierarchical Residual Reinforcement Learning）：分层残差强化学习
- 层1：姿态控制（LQR + TD3残差补偿）
- 层2：位置控制（Stanley + RL补偿）

## 自行车动力学模型（Carvallo-Whipple模型简化版）

### 坐标系
- δ：前轮转向角
- θ：车身倾斜角（roll）
- v：车速（论文中取4m/s）

### 动力学方程（非线性）

H·θ̈ = g·sinθ - (v/L)²·tanδ·(√(L² + L₁²·tan²δ) + Lg)·cosθ

其中：Lg = L(m_f·r_f + m_r·r_r)/m

### 转弯半径
R_r = L/tanδ
R_f = L/sinδ
R_c = √(R_r² + L²)·sign(δ)

### 离心力矩
F_ω = m·ω²·R_c·sign(δ)
τ_ω = F_ω·H·cosθ·sign(δ)

### 重力矩
τ_g = m·g·H·sinθ

### 转动惯量
I = m·H²

### 力矩平衡方程
I·θ̈ = τ_g - τ_ω - M_g

## 线性化（小角度近似）

近似条件：sinθ≈θ, cosθ≈1, tanθ≈θ, tanδ≈δ

线性化后：
H·θ̈ = g·θ - (v/L)²·δ·(√(L² + L₁²·δ²) + Lg)

## 状态空间模型

状态：x = [θ, θ̇]ᵀ
输入：u = (v/L)²·tanδ

ẋ = Ax + Bu

A = [0,    1    ]
    [g/H,  0    ]

B = [0           ]
    [-(L+Lg)/H  ]

## 可控性分析

可控性矩阵：C = [B, AB]
rank(C) = 2（当L+Lg ≠ 0时）

系统特征值：λ = ±√(g/H)
- 正实数极点 → 开环不稳定
- 但系统完全可控（可通过转向输入稳定）

## LQR控制器设计

性能指标：J = ∫(eᵀQe + uᵀRu)dt

参数：
- Q = [30, 0; 0, 1]  （θ权重30，θ̇权重1）
- R = 1

增益：K = R⁻¹BᵀP（P为Riccati方程解）

控制律：δ_LQR = arctan[L²/v²·(F·x_d + K·e)]

## 实验参数

仿真环境：PyBullet + OpenAI Gym
- 步长：10ms
- 车速：4m/s

### 物理参数
| 参数 | 值 | 说明 |
|------|-----|------|
| H | 0.63m | 质心高度 |
| L | 1.17m | 轴距 |
| L1 | 0.61m | 前轴到质心距离 |
| m | 12.35kg | 车身质量 |
| m_f | 2.40kg | 前轮质量 |
| m_r | 2.65kg | 后轮质量 |
| r_f | 0.32m | 前轮半径 |
| r_r | 0.32m | 后轮半径 |

### LQR参数
Q = [30, 0; 0, 1], R = 1

### Stanley参数
k = 0.6

## 控制架构

传统方法（论文Ch2）：
- LQR：纵向/姿态控制（内环）
- Stanley：横向/路径跟踪（外环）

强化学习方法（论文Ch3）：
- TD3（Twin Delayed DDPG）
- 双Critic网络、延迟策略更新、目标策略平滑

分层残差方法（论文Ch4）：
- 姿态层：LQR + TD3残差补偿（解决模型简化导致的稳态误差）
- 位置层：Stanley + RL补偿（提升弯道跟踪精度）
- 训练时间：从8210s降至1596s，500轮训练0次倾覆

## 与我们项目的对比

论文硬件：IMU + 编码器 + Nvidia Jetson AGX Xavier
我们硬件：N100 IMU + 布瑞特FOC电机 + Arduino Nano ESP32

关键差异：
1. 论文用仿真+实车验证，我们目前在调LQR阶段
2. 论文的状态空间是2维（θ, θ̇），我们的状态空间是12维
3. 论文的LQR用于姿态控制，我们的LQR用于横向控制（mode2）
