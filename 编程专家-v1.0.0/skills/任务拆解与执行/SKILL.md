---
name: 任务拆解与执行
description: >
  将复杂编程需求拆分为原子任务，按依赖关系分组为Wave执行，每个任务独立上下文，确保验证闭环。
  解决AI长对话中的context rot问题，让复杂工程稳定交付。
  触发词："拆解任务"、"任务规划"、"怎么执行"、"分步骤实现"、"执行计划"、
  "wave执行"、"原子任务"、"任务拆分"、"分阶段开发"、"执行流程"、"任务清单"。
argument-hint: "描述复杂需求或已有spec，要求拆解为可执行任务"
name_en: "task-decomposition-and-execution"
description_en: >
  Break complex programming requirements into atomic tasks, group by dependencies into Waves,
  isolate context per task, ensure verification closure. Solves context rot in long AI conversations.
  Trigger phrases: "break down tasks", "task planning", "execution plan", "wave execution",
  "atomic tasks", "task decomposition", "phased development".
---

# /任务拆解与执行 -- 复杂任务拆解与Wave执行

> 如遇到不熟悉的占位符，参见 [CONNECTORS.md](../../CONNECTORS.md)。

**独立能力（无需连接器）**

- 将复杂需求拆分为2-5个原子任务
- 按依赖关系分组为Wave（并行/串行）
- 每个任务独立上下文管理
- 验证闭环（verify before mark done）

## 调用方式

```
/任务拆解与执行 <复杂需求或spec>
```

拆解以下需求为可执行任务：@$1

## 输入要求

1. **需求或spec**（必填）：需要实现的功能描述或已有spec
2. **现有代码**（可选）：相关代码片段或文件列表
3. **约束条件**（可选）：时间、性能、依赖限制

## 执行流程

### 第一步：需求分析

- 理解核心目标和边界
- 识别隐含依赖（如"用户系统"依赖"数据库表已存在"）
- 识别风险点（复杂算法、第三方集成、性能瓶颈）

### 第二步：原子任务拆解

将复杂需求拆分为2-5个原子任务。每个任务必须满足：
- **单一职责**：只解决一个明确问题
- **可独立完成**：一个context window内可完成
- **可验证**：有明确的完成标准
- **可回滚**：失败时不影响其他任务

**任务结构（XML格式）**：
```xml
<task type="auto|human-verify|decision">
  <name>[任务名称]</name>
  <files>[涉及文件列表]</files>
  <action>
    [具体执行步骤]
  </action>
  <verify>
    [验证方法：测试命令/检查清单/人工确认]
  </verify>
  <done>
    [完成标准：什么状态算完成]
  </done>
</task>
```

### 第三步：Wave分组

按依赖关系将任务分组：

```
Wave 1（并行，无依赖）
├── Task 1.1: [任务A]
└── Task 1.2: [任务B]

Wave 2（依赖Wave 1）
├── Task 2.1: [任务C，依赖1.1]
└── Task 2.2: [任务D，依赖1.2]

Wave 3（依赖Wave 2）
└── Task 3.1: [任务E，依赖2.1和2.2]
```

**分组原则**：
- 无依赖的任务 → 同一Wave，可并行
- 有依赖的任务 → 后续Wave，必须串行
- 可能文件冲突的任务 → 同一Wave内串行或合并为一个任务

### 第四步：上下文隔离

执行单个任务时，只加载必要上下文：

```
任务上下文 = {
  spec: [相关requirement和scenario],
  design: [相关技术决策],
  files: [该任务需要读写的文件],
  decisions: [影响该任务的历史决策],
  previous_summary: [前置Wave的任务summary]
}
```

**禁止加载**：
- 无关模块的代码
- 已完成的无关任务细节
- 未决但无关的讨论

### 第五步：执行与验证闭环

每个任务执行后：

1. **执行**：按action完成代码修改
2. **自测**：运行verify中的验证方法
3. **记录summary**：
   ```
   ## Task Summary: [任务名]
   
   **完成状态**: [完成/部分完成/失败]
   **修改文件**: [文件列表]
   **关键决策**: [执行中做出的决策]
   **偏差说明**: [与plan的差异及原因]
   **遗留问题**: [未解决的问题]
   ```
4. **验证通过**：标记done，进入下一任务
5. **验证失败**：修复或回滚，重新执行

## 输出格式

```
## 任务拆解报告

### 需求概述
[一句话总结]

### 任务列表

#### Wave 1（并行）
```xml
<task type="auto">
  <name>...</name>
  <files>...</files>
  <action>...</action>
  <verify>...</verify>
  <done>...</done>
</task>
```

#### Wave 2（依赖Wave 1）
...

### 执行建议
- 优先执行Wave 1，并行推进
- Wave 2等Wave 1全部完成后再开始
- 每个任务完成后立即验证

### 风险点
- [风险1及缓解措施]
```

## 质量标准

- 每个任务必须可在单个context window完成（建议不超过200行代码变更）
- 每个任务必须有明确的verify方法，不能是"看起来对就行"
- Wave分组必须明确标注依赖关系
- 任务summary必须记录偏差，不能假装一切按计划进行
- 失败任务必须说明原因，不能默默跳过
- 优先"垂直切片"（端到端功能）而非"水平分层"（全部模型→全部API）

## 关联Skill

- **Spec驱动开发** — 拆解前用 `/Spec驱动开发` 确保需求已对齐
- **代码生成** — 每个task可用 `/代码生成` 实现具体代码
- **代码审查** — 每个task完成后用 `/代码审查` 检查质量
- **项目记忆管理** — 将task summary和决策记录到项目记忆
