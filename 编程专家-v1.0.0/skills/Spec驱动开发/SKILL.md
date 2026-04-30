---
name: Spec驱动开发
description: >
  在编码前对齐需求规格，使用OpenSpec的artifact flow和delta spec思想，将模糊意图转化为可审核、可复用、可迭代的项目资产。
  触发词："写spec"、"对齐需求"、"spec驱动"、"需求规格"、"设计规格"、"先写spec"、
  "需求文档"、"功能规格"、"变更规格"、"delta spec"、"spec review"、"规格评审"。
argument-hint: "描述需求或变更内容，可附带现有spec上下文"
name_en: "spec-driven-development"
description_en: >
  Align on requirements before coding using OpenSpec's artifact flow and delta spec philosophy.
  Convert vague intent into reviewable, reusable, iterable project assets.
  Trigger phrases: "write spec", "spec driven", "requirement spec", "design spec", "delta spec".
---

# /Spec驱动开发 -- 需求规格对齐

> 如遇到不熟悉的占位符，参见 [CONNECTORS.md](../../CONNECTORS.md)。

**独立能力（无需连接器）**

- 将模糊需求转化为结构化spec
- 生成轻量级delta spec（ADDED/MODIFIED/REMOVED）
- 提供artifact flow引导（proposal → specs → design → tasks）
- 编码前spec验证

## 调用方式

```
/Spec驱动开发 <需求描述>
```

为以下需求编写规格：@$1

## 输入要求

1. **需求描述**（必填）：需要实现的功能或变更
2. **项目上下文**（可选）：现有系统状态、相关模块
3. **已有spec**（可选）：如果已有spec需要增量修改
4. **约束条件**（可选）：性能、安全、兼容性要求

## 执行流程

### 第一步：明确意图（Proposal）

用3句话以内说明：
- **Intent**：为什么要做这个变更
- **Scope**：变更范围（In scope / Out of scope）
- **Approach**：大致技术方向

**示例**：
```
Intent: 用户请求添加暗黑模式以减少夜间使用时的眼疲劳
Scope: In scope - 主题切换、系统偏好检测、localStorage持久化
        Out of scope - 自定义颜色主题、按页面覆盖主题
Approach: CSS自定义属性 + React Context管理状态
```

### 第二步：编写Delta Spec

根据变更类型选择对应section：

#### ADDED Requirements（新增功能）

```markdown
## ADDED Requirements

### Requirement: [需求名称]
The system SHALL [具体行为描述].

#### Scenario: [场景名称]
- GIVEN [前置条件]
- WHEN [用户操作/系统事件]
- THEN [预期结果]
- AND [额外预期结果]
```

#### MODIFIED Requirements（修改现有功能）

```markdown
## MODIFIED Requirements

### Requirement: [需求名称]
The system MUST [新行为描述].
(Previously: [原行为描述])

#### Scenario: [场景名称]
- GIVEN [前置条件]
- WHEN [用户操作/系统事件]
- THEN [新预期结果]
```

#### REMOVED Requirements（移除功能）

```markdown
## REMOVED Requirements

### Requirement: [需求名称]
[移除原因说明]
```

### 第三步：编写Design（技术方案）

```markdown
## Design: [变更名称]

### Technical Approach
[技术实现思路，1-2段]

### Architecture Decisions
- Decision: [决策点]
  - Reason: [选择理由]

### File Changes
- `[文件路径]` (new/modified/deleted)
```

### 第四步：生成Tasks（实现清单）

```markdown
## Tasks

### Wave 1（无依赖，可并行）
- [ ] Task 1.1: [具体任务]
- [ ] Task 1.2: [具体任务]

### Wave 2（依赖Wave 1）
- [ ] Task 2.1: [具体任务]
```

### 第五步：编码前Spec验证

在开始编码前，检查：
- [ ] 每个Requirement是否有至少一个Scenario
- [ ] 每个Scenario是否可测试（有明确的Given/When/Then）
- [ ] 成功标准是否明确（"系统应该..."而非"系统可能..."）
- [ ] 变更范围是否聚焦（没有无意识扩散）

**如无spec，提示**：
```
⚠️ 未检测到spec。建议先完成spec对齐再编码。
用 `/Spec驱动开发` 生成spec，或提供已有spec。
```

**如有spec，作为编码依据**：
```
✓ 检测到spec。编码时将严格按以下scenario实现：
- [Scenario列表]
```

## 输出格式

```
## Spec: [变更名称]

### Proposal
Intent: [意图]
Scope: [范围]
Approach: [方向]

### Delta Spec

## ADDED Requirements
...

## MODIFIED Requirements
...

## REMOVED Requirements
...

### Design
...

### Tasks
...

### Spec验证
- [ ] Requirements可测试
- [ ] Scenarios覆盖主路径和边界
- [ ] 成功标准明确
```

## 质量标准

- Spec是**行为契约**，不是实现计划（不写具体类名/函数名）
- 使用RFC 2119关键词：MUST/SHALL（绝对要求）、SHOULD（建议）、MAY（可选）
- 每个Requirement至少一个Scenario
- Scenario使用Given/When/Then格式，可转化为自动化测试
- Delta spec只描述变更，不重复未变更的内容
- 保持轻量：大多数变更使用Lite spec（简短需求+验收检查），高风险变更才用Full spec

## 关联Skill

- **任务拆解与执行** — spec完成后用 `/任务拆解与执行` 将tasks转为可执行计划
- **代码生成** — 编码时用spec作为验收依据
- **代码审查** — 审查时检查实现是否符合spec
- **项目记忆管理** — 将spec和design决策记录到项目记忆
