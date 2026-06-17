# 记忆档案（长期存储）模板
# 当内部memory工具满时，将详细信息迁移到此文件
# 内存只保留索引指向此文件

## 使用方式
1. 内存满时 → 将详细条目写入此文件
2. 内存中只保留"详细规则见memory-archive.md"
3. 需要时 → read_file("D:/openclaw-hermes/memory-archive.md")
4. session_search可替代部分长期记忆

## 模板结构

### [分类1名称]
- 详细规则/配置/历史信息
- 条目1
- 条目2

### [分类2名称]
- 详细规则/配置/历史信息

### [分类N名称]
- ...

## 压缩技巧
- 合并重复条目（如多个Gateway配置→一条）
- 用"详见memory-archive.md"替代完整内容
- session_search按需回溯历史对话
- 定期清理已过时的条目
