---
name: planning-before-execution
description: 在任务执行前进行框架规划, 明确步骤、资源、预期产出, 减少因执行偏差导致的token浪费和重试。
allowed-tools: Bash(python:*), Bash(curl:*), Bash(wget:*)
---

# planning-before-execution

## 分类

A类-降Token

## 功能

任务执行前先输出结构化规划:
1. 步骤拆解
2. 每步所需工具
3. 预期产出
4. 风险预判
规划完成后确认再执行。

## 使用方式

在任务中调用此 skill 以启用对应能力。
