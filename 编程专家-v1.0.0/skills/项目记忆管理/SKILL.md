---
name: 项目记忆管理
description: >
  捕获会话上下文、技术决策和项目规范，实现跨会话项目记忆沉淀与恢复。
  采用渐进式披露策略，让新会话快速恢复关键约束。
  触发词："记录会话"、"项目记忆"、"session总结"、"决策记录"、"项目规范"、
  "跨会话"、"记忆恢复"、"上下文恢复"、"项目知识库"、"记录决策"、"规范沉淀"。
argument-hint: "描述需要记录的内容类型：session总结、决策记录、规范沉淀"
name_en: "project-memory-management"
description_en: >
  Capture session context, technical decisions, and project conventions for cross-session continuity.
  Use progressive disclosure to let new sessions quickly recover key constraints.
  Trigger phrases: "record session", "project memory", "session summary", "decision log",
  "project conventions", "cross-session", "memory recovery", "context restore".
---

# /项目记忆管理 -- 跨会话项目记忆沉淀

> 如遇到不熟悉的占位符，参见 [CONNECTORS.md](../../CONNECTORS.md)。

**独立能力（无需连接器）**

- 生成结构化session summary
- 记录技术决策上下文
- 沉淀项目特定规范
- 新会话渐进式记忆恢复

## 调用方式

```
/项目记忆管理 <记录类型>
```

记录以下内容：@$1

## 输入要求

1. **记录类型**（必填）：session总结 / 决策记录 / 规范沉淀 / 记忆恢复
2. **内容详情**（必填）：具体要记录的信息
3. **项目标识**（可选）：项目名称或标识符

## 执行流程

### 模式一：会话结束记录（Session Summary）

会话结束时生成结构化summary：

```markdown
## Session Summary

**日期**: [YYYY-MM-DD]
**会话目标**: [本次会话原计划完成什么]

### 已完成
- [任务1]: [简要说明] → [相关文件]
- [任务2]: [简要说明] → [相关文件]

### 关键决策
- **决策**: [决策内容]
  - **上下文**: [为什么做这个决策]
  - **影响**: [影响哪些后续工作]

### 遗留问题 / Blockers
- [问题1]: [描述] → [下一步行动]

### 下一步计划
1. [下一步任务]
2. [下一步任务]

### 规范更新
- [新发现的项目规范]
```

### 模式二：决策记录（Decision Record）

重要技术决策时记录：

```markdown
## Decision Record: [决策名称]

**日期**: [YYYY-MM-DD]
**问题**: [需要解决什么问题]

### 选项分析
| 选项 | 优势 | 劣势 | 复杂度 |
|------|------|------|--------|
| [选项A] | ... | ... | 低/中/高 |
| [选项B] | ... | ... | 低/中/高 |

### 决策
**选择**: [最终选项]
**理由**: [为什么选这个]
**Trade-offs**: [接受了什么代价]

### 影响范围
- [影响的模块/文件]
- [需要同步更新的文档]

### 撤销条件
[什么情况下可以重新考虑这个决策]
```

### 模式三：规范沉淀（Convention Capture）

发现项目特定规范时记录：

```markdown
## Project Convention: [规范名称]

**类型**: [编码规范/命名规范/架构约束/工具配置]
**适用范围**: [哪些模块/文件适用]

### 规范内容
[具体规则]

### 示例
**正确**:
```[代码示例]```

**错误**:
```[代码示例]```

### 发现来源
[哪次会话/哪个任务中发现]
```

### 模式四：新会话记忆恢复（Progressive Disclosure）

新会话开始时，按三层加载记忆：

**Layer 1: Metadata（~50 tokens）**
```
项目: [名称]
当前阶段: [阶段]
活跃任务: [任务名]
上次会话: [日期]
```

**Layer 2: Body（~200 tokens）**
```
## 上次Session Summary
[最近一次的summary核心内容]

## 活跃决策
- [与当前任务相关的决策]
```

**Layer 3: References（按需加载，~500 tokens each）**
```
## 相关决策记录
[与当前任务相关的完整决策记录]

## 相关规范
[与当前任务相关的项目规范]
```

**加载策略**：
1. 始终加载Layer 1
2. 如果当前任务与上次会话连续，加载Layer 2
3. 如果涉及历史决策或规范，按需加载Layer 3
4. 总token预算控制在1000以内，避免context rot

## 输出格式

根据模式输出对应格式（见上文）。

通用原则：
- 使用结构化Markdown，便于后续检索
- 每条记录包含时间戳
- 引用具体文件路径，不泛泛而谈
- 避免重复：新规范与已有规范冲突时，标注替代关系

## 质量标准

- Session summary必须在会话结束时立即生成，不能拖延
- 决策记录必须包含"撤销条件"，避免过早固化
- 规范沉淀必须有正/反例，不能只有文字描述
- 记忆恢复时优先加载与当前任务最相关的内容
- 总记忆加载量控制在1000 tokens以内，超过时优先丢弃最旧的记录
- 项目规范冲突时，以时间最近的为准，并标注冲突

## 关联Skill

- **Spec驱动开发** — 将spec和design决策记录到项目记忆
- **任务拆解与执行** — 将task summary记录到项目记忆
- **技术选型** — 选型决策自动记录到项目记忆
- **代码生成** — 编码前加载项目规范，编码后记录新发现规范
