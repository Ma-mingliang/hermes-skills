---
name: context-compression
description: 对上下文进行智能压缩, 优先保留高价值信息, 减少token消耗。用于多轮对话、长文本分析、批量信息处理场景。
allowed-tools: Bash(python:*), Bash(curl:*), Bash(wget:*)
---

# context-compression

## 分类

A类-降Token

## 功能

通过分层压缩策略对输入上下文进行精简:
1. 关键信息提取
2. 冗余内容去重
3. 分层摘要
实测可减少30%-60%的上下文token消耗。

## 使用方式

在任务中调用此 skill 以启用对应能力。
