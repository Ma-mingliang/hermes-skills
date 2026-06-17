# 横向模式串级PID实现细节

## 实现日期
2026-05-30

## 修改文件
1. `bike/src/mode1/mode1.cpp` - 添加速度外环
2. `bike/src/mode1/mode1.h` - 更新接口说明
3. `bike/src/RobotLink/RobotContext.h` - 添加速度环参数定义

## 控制结构

```
throttle ──────────────────────────────────────┐
                                              ↓
motor1Erpm ──┐                                 [速度误差]
            ├─→ 速度PI ─→ 目标角度补偿 ──┐    ↓
motor2Erpm ──┘                            │  [角度误差]
                                          ↓    ↓
mechanicalBase + mechanicalTrim ───→ targetAngle
                                              ↓
                                  [角度误差] ─→ PD ─→ 电流命令
                                       ↑ 实际角度 ↑ 角速度
                                    pitchDeg  pitchRateDeg
```

## 代码实现要点

### 速度外环（PI控制器）
```cpp
// 计算实际速度（两轮平均）
const float actualSpeed = 0.5f * ((float)motor1Erpm + (float)motor2Erpm);

// 低通滤波
gFilteredSpeed = lowPassFilter(actualSpeed, gFilteredSpeed, speedFilterAlpha);

// 速度误差
float speedError = speedTarget - gFilteredSpeed;

// 速度环积分（带限幅）
gSpeedIntegral += speedError;
gSpeedIntegral = clampFloat(gSpeedIntegral, -speedMaxIntegral, speedMaxIntegral);

// 速度环输出（目标角度补偿量，单位：度）
const float speedOutput = speedKp * speedError + speedKi * gSpeedIntegral;
```

### 直立内环（PD控制器）
```cpp
// 目标角度 = 机械基准 + 人工修正 + 速度环补偿
const float targetAngle = gMechanicalAngleBase + mechTrim + speedOutput;

// 角度误差
const float angleError = targetAngle - pitch;

// 直立环输出
const float balanceOutput = balanceKp * angleError + balanceKd * pitchRate;
```

## 参数默认值

| 参数 | 默认值 | 说明 |
|------|--------|------|
| SPEED_KP | 0.5 | 速度环比例系数 |
| SPEED_KI | 0.01 | 速度环积分系数 |
| SPEED_MAX_INTEGRAL | 5.0 | 积分限幅（度） |
| SPEED_FILTER_ALPHA | 0.1 | 速度滤波系数 |
| SPEED_TARGET | 0.0 | 目标速度（ERPM） |
| BALANCE_KP | 59.0 | 直立环比例系数 |
| BALANCE_KD | 0.0 | 直立环微分系数 |
| MAX_OUTPUT_CURRENT | 1000 | 输出电流限幅（10mA） |
| START_CURRENT | 30 | 最小启动电流（10mA） |
| CURRENT_DEADBAND | 15 | 电流死区阈值（10mA） |

## 调试信息

调试帧中新增的字段：
- `speedOutput`: 速度环输出（角度补偿量）
- `speedIntegral`: 速度环积分项
- `targetAngle`: 最终目标角度（含速度环补偿）
- `actualSpeed`: 实际速度（两轮平均ERPM）

## 调参建议

1. **先调直立环**：确保车体能在人工扶持下保持平衡
   - 从较小的KP开始（如30），逐步增大
   - 添加适当的KD提供阻尼

2. **再调速度环**：在直立环稳定的基础上添加速度控制
   - 从较小的KP开始（如0.1），观察速度响应
   - 添加KI消除稳态误差
   - 调整积分限幅防止积分饱和

3. **滤波系数**：根据速度反馈的噪声水平调整
   - 噪声大：减小alpha（如0.05）
   - 响应慢：增大alpha（如0.2）

## 下一步

- 烧录固件到ESP32
- 在实车上测试串级PID控制效果
- 根据测试结果调整参数
