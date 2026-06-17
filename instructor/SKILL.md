---
name: instructor
description: 通过Pydantic schema约束LLM输出格式, 确保结构化数据符合预期, 减少格式偏差和重试。
allowed-tools: Bash(python:*), Bash(curl:*), Bash(wget:*)
---

# instructor

## 分类

B类-约束行为

## 功能

结构化输出控制:
1. 定义输出schema
2. 强制符合schema
3. 自动重试格式不符的响应

## 使用方式

在任务中调用此 skill 以启用对应能力。
