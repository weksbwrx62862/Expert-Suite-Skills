# Task 编排状态机：status/next/advance/log

## Background

### 现状

Trellis 的 task 系统有 parent/child 关系和 `current_phase` + `next_action[]` 状态机，但这两个能力是割裂的：

- **next_action 状态机**：只在单 task 内部工作（implement → check → finish → create-pr）
- **parent/children**：只是数据关系，没有编排能力（不知道"下一个该执行哪个 child"）

这导致任何需要"多子任务按序执行"的场景都必须在 prompt 里硬编码编排逻辑：

| 场景 | 现在怎么做 | 问题 |
|------|-----------|------|
| start.md 执行阶段 | prompt 写死 "Step 8: implement → Step 9: check → Step 10: complete" | ~200 行 prompt，AI 必须记住流程，compaction 后可能忘 |
| autopilot 长时间执行 | 生成 TASK-PROMPT.md + PROGRESS.md，AI 手动维护状态 | prompt 臃肿，PROGRESS.md 靠 AI 手写（不可靠） |
| dispatch agent | 自己解析 next_action 数组 | 逻辑散落在 agent prompt 里 |

### 核心问题

**"AI 需要记住的流程"应该变成"AI 随时可以查询的状态"。**

prompt 里的编排逻辑越长，被 context compaction 吃掉的风险越大。如果状态在磁盘上（task.json），AI 只需一条命令就能知道"下一步做什么"——不需要记住任何流程。

## Goal

扩展 `task.py` 支持 parent/child 编排状态机，通过 `status`/`next`/`advance`/`log` 四个命令将编排逻辑从 prompt 下沉到 Trellis 基础设施。

## Design Decisions

> Codex review 提出的关键问题，在实现前必须确定。

### D1: Phase 推进权责（Critical）

**问题**：现有 hook（inject-subagent-context.py）在 subagent 调用时自动更新 `current_phase`。如果 `advance` 也能更新 `current_phase`（无 children 场景），两个写入者会导致 phase 跳跃。

**决策**：**分层所有权，互不越界。**
- **Child 内部 phase**（implement→check→finish）：由 hook 独占管理，`advance` 不碰
- **Parent 层 child 切换**（child-1→child-2→child-3）：由 `advance` 独占管理
- **无 children 单任务**：`advance` 不操作 `current_phase`，返回当前 phase 信息供 AI 调用对应 agent（phase 推进仍由 hook 完成）

这意味着 `advance` 在无 children 场景下是**只读查询 + child 切换**，不写 `current_phase`。

### D2: 路径 Normalize（High）

**问题**：`.current-task` 可能存绝对路径或相对路径，`children[]` 存的是目录名。比较时可能误判。

**决策**：**统一用相对于 repo root 的路径比较。**
- 比较前对 `.current-task` 值和 child 路径都做 normalize：去除 trailing slash，resolve 为相对路径
- 复用现有 `resolve_task_dir()` 函数（task.py:163-189 已有三种格式的解析）

### D3: Parent Status 生命周期（High）

**问题**：`task.py start` 目前不更新 task status 字段。parent 的 `planning → in_progress → completed` 转换规则未定义。

**决策**：**`advance` 自动管理 parent status。**

| 事件 | Parent status 变更 |
|------|-------------------|
| 第一个 child 被 activate | `planning` → `in_progress` |
| 所有 children completed | → `completed`，设 `completedAt` |
| 中间状态 | 保持 `in_progress` |

Child status 也由 `advance` 管理：`advance` 标记当前 child 为 `completed`。

### D4: 嵌套 Children 深度（High）

**问题**：`status` 说"递归读 children"，但 `next/advance` 只处理直接 children。嵌套行为未定义，有环风险。

**决策**：**本版只支持 depth=1（直接 children）。**
- `status`：只读直接 children，不递归
- `next/advance`：只处理直接 children
- 如果 child 自身也有 children → 忽略（不展开）
- 未来版本可扩展，但要加 cycle detection

### D5: JSON Schema 和 Exit Code（Medium）

**决策**：

| 场景 | Exit code | Stdout |
|------|-----------|--------|
| 成功 | 0 | JSON 结果 |
| 无 children（对 advance/next） | 0 | 单任务模式的 JSON |
| Task dir 不存在 | 1 | Stderr 错误消息 |
| .current-task 不属于 parent | 1 | Stderr 错误消息 |
| Child dir 不存在 | 0 | 跳过 + stderr 警告，继续处理其余 |

所有命令 JSON 输出到 stdout，错误/警告到 stderr。`--json` flag 对 `status` 命令确保纯 JSON（无 emoji 装饰）。

### D6: Status 值兼容（Medium）

**问题**：现有代码同时认 `completed` 和 `done`。

**决策**：**判断完成时用 `status in ("completed", "done")`。** 写入时统一用 `completed`。

### D7: 内部函数重构前提（Critical）

**问题**：PRD 提到复用 `do_start()/do_finish()`，但这些内部函数不存在，目前只有 `cmd_start/cmd_finish` CLI handlers。

**决策**：**实现时先从 `cmd_start`/`cmd_finish` 提取共享 helper。**
- 提取 `_activate_task(task_dir)` 和 `_deactivate_task(clear_session=True)` 内部函数
- `_deactivate_task` 的 `clear_session` 参数：`cmd_finish` 调时传 `True`（session 结束），`cmd_advance` 调时传 `False`（child 切换，session 仍在继续）
- `cmd_start`、`cmd_finish`、`cmd_advance` 都调这两个 helper
- 这是实现的第一步，不是单独 task

### D8: 平台感知 — `.current-session` 文件（Medium）

**问题**：`next` 返回 `{"action": "implement"}`，但不同平台的执行方式不同。Claude Code 调 subagent（hooks 自动注入 context），Cursor 等无 hooks 平台需要手动读 spec。如果 `next` 能根据平台返回不同指引，AI 不需要自己判断。

**决策**：**不改 `.current-task`，新增 `.current-session` 文件。**

```
.trellis/.current-task       ← 不变，单行路径
.trellis/.current-session    ← 新增 JSON
```

```json
{"platform": "claude", "started_at": "2026-03-10T14:30:00"}
```

**写入时机**：
- `task.py start --platform <name>` 时写入（手动指定，无 hooks 平台的 fallback）
- session-start hook 触发时自动写入（Claude Code / iFlow，hook 知道自己的平台）

**清除时机**：
- **顶层 `cmd_finish`**（用户或 AI 显式调用 `task.py finish`）清除 `.current-task` 和 `.current-session`
- **`advance` 内部的 `_deactivate_task()`**：只清除 `.current-task`，**不清除** `.current-session`
  - 理由：`advance` 做的是 child 切换（finish child-A → start child-B），session 没结束，平台没变
  - 如果 `_deactivate_task()` 也清了 `.current-session`，紧接着的 `_activate_task()` 就丢失了平台信息，后续 `next` 无法输出正确的 execution/hint
- 实现方式：`_deactivate_task(clear_session=False)`，`cmd_finish` 调时传 `clear_session=True`

**`next` 根据 platform 的输出差异**：

```json
// Claude Code / iFlow（有 hooks）
{
  "action": "implement",
  "child_dir": ".trellis/tasks/03-10-s2-core",
  "execution": "subagent",
  "hint": "Call Agent(subagent_type='implement'). Hooks inject context automatically."
}

// Cursor 等（无 hooks）
{
  "action": "implement",
  "child_dir": ".trellis/tasks/03-10-s2-core",
  "execution": "direct",
  "context_file": ".trellis/tasks/03-10-s2-core/implement.jsonl",
  "hint": "Read context_file for spec paths, then implement directly."
}
```

**所有 action 的 execution/hint 映射**：

| action | 有 hooks（claude/iflow） | 无 hooks（cursor 等） |
|--------|-------------------------|---------------------|
| `implement` | `execution: "subagent"`, hint: "Call Agent(subagent_type='implement')" | `execution: "direct"`, hint: "Read {context_file} for specs" |
| `check` | `execution: "subagent"`, hint: "Call Agent(subagent_type='check')" | `execution: "direct"`, hint: "Read {context_file}, review changes" |
| `finish` | `execution: "command"`, hint: "Run task.py finish" | 同左 |
| `create-pr` | `execution: "command"`, hint: "Run task.py create-pr or gh pr create" | 同左 |
| `all_done` | 无 execution/hint（status 自带语义） | 同左 |

`finish` 和 `create-pr` 不区分平台，因为它们是直接的命令调用，不涉及 hooks。

**无 `.current-session` 时**（向后兼容）：默认按有 hooks 模式输出（`execution: "subagent"`）。

**现有代码影响**：**零改动。** `.current-task` 格式不变，4 处读取代码不需要任何修改。

**需要更新的文件**：

| 文件 | 改动 |
|------|------|
| `.trellis/scripts/common/paths.py` | 新增 `get_current_platform()` / `set_current_session()` / `clear_current_session()` |
| `.trellis/scripts/task.py` | `cmd_start` 加 `--platform` 参数，调 `set_current_session()`；`cmd_finish` 加调 `clear_current_session()` |
| `.trellis/.gitignore` | 新增 `.current-session` |
| `packages/cli/src/templates/trellis/gitignore.txt` | 同步新增 `.current-session` |
| `packages/cli/src/templates/markdown/gitignore.txt` | 同步新增 `.current-session` |
| `packages/cli/src/constants/paths.ts` | 新增 `CURRENT_SESSION` 常量（CLI 更新模板时需要感知） |

**Platform 值约定**：

| Platform | 值 | 有 hooks |
|----------|------|---------|
| Claude Code | `claude` | ✅ |
| iFlow | `iflow` | ✅ |
| Cursor | `cursor` | ❌ |
| OpenCode | `opencode` | ❌ |
| Codex | `codex` | ❌ |
| Kilo | `kilo` | ❌ |
| Kiro | `kiro` | ❌ |
| Gemini CLI | `gemini` | ❌ |
| Antigravity | `antigravity` | ❌ |

---

## Architecture

### 从指令式到状态机

```
现在（指令式 prompt）：
  prompt 告诉 AI "做 A → 做 B → 做 C"
  AI 必须在上下文里保持完整流程记忆

以后（状态机查询）：
  AI: "python3 task.py next <parent>"  → {"action": "implement", "child": "..."}
  AI: 执行
  AI: "python3 task.py advance <parent>"  → {"action": "check", "child": "..."}
  AI: 执行
  ...直到 all_done
```

### 两层状态机

```
Parent 编排层:   child-1 ──→ child-2 ──→ child-3 ──→ done
                    │            │            │
                    ▼            ▼            ▼
Child 执行层:   implement   implement   implement
                   ↓            ↓            ↓
                 check        check        check
                   ↓            ↓            ↓
                 finish       finish       finish
```

- **上层**：`task.py next/advance` 驱动 child 间切换
- **下层**：现有 hooks 驱动 child 内部的 phase 推进（current_phase + next_action）
- 两层共用同一套 task.json 数据，不引入新数据结构

### 单任务也兼容

对于没有 children 的单任务，`next` 直接返回该 task 自身的 next_action 状态：

```bash
$ python3 task.py next .trellis/tasks/03-10-simple-task
{"status": "in_progress", "action": "implement", "phase": 1, "total_phases": 4}
```

统一接口，无论单任务还是多子任务。

## Requirements

### R1: `task.py status <task-dir>` — 状态概览

从 task 及其 children 的 task.json 计算全局状态。

**有 children 时输出：**
```
Parent: 03-10-migrate-cmd (in_progress) [1/3 done]

Subtasks:
  ✅ 03-10-s1-types      completed    phase: 4/4
  🔄 03-10-s2-core       in_progress  phase: 2/4  ← current
  ⬜ 03-10-s3-tests      planning     phase: 0/4

Current: 03-10-s2-core (check)
Next: 03-10-s3-tests

Recent log:
  [14:30] decision: 选择方案 A 因为更简单
  [15:00] error: Lint failed on foo.ts:42
```

**无 children 时输出：**
```
Task: 03-10-simple-task (in_progress)
Phase: 2/4 (check)
Next: finish
```

要求：
- 读 task.json 的 children 数组，读每个**直接** child 的 task.json（不递归，见 D4）
- 与 `.current-task` 比较标记当前激活的 child（路径 normalize，见 D2）
- 完成判断用 `status in ("completed", "done")`（见 D6）
- 尾部附最近 3 条 `run.log.jsonl` 日志（如有）
- `--json` flag 输出纯 JSON（无 emoji），schema 见 D5

### R2: `task.py next <task-dir>` — 查询下一步

返回状态机的下一个动作。

**有 children 时逻辑：**
1. 按 `children[]` 数组顺序遍历
2. 找第一个 `status not in ("completed", "done")` 的 child（见 D6）
3. 读该 child 的 `current_phase` 和 `next_action`
4. 返回（以 Claude Code 为例，Cursor 等平台 execution/hint 不同，见 D8）：
   ```json
   {
     "status": "in_progress",
     "child_dir": ".trellis/tasks/03-10-s2-core",
     "child_title": "实现核心逻辑",
     "action": "check",
     "phase": 2,
     "total_phases": 4,
     "needs_activation": true,
     "execution": "subagent",
     "hint": "Call Agent(subagent_type='check'). Hooks inject context automatically."
   }
   ```
5. 所有 children 完成 → `{"status": "all_done", "completed": 3, "total": 3}`

**无 children 时逻辑：**
1. 读自身 `current_phase` 和 `next_action`
2. 返回：
   ```json
   {
     "status": "in_progress",
     "action": "implement",
     "phase": 1,
     "total_phases": 4
   }
   ```
3. 所有 phase 完成 → `{"status": "all_done"}`

**边界情况：**
- `children` 中某个 dir 不存在 → 跳过并 stderr 警告，exit 0（见 D5）
- `needs_activation`: normalize 后 `child_dir != .current-task` 时为 true（见 D2）
- 完成判断用 `status in ("completed", "done")`（见 D6）
- parent 没有 children 且自身已 completed → `all_done`

### R3: `task.py advance <task-dir>` — 推进状态机

完成当前步骤，激活下一个。

**有 children 时逻辑：**
1. 读 `.current-task`
2. 如果当前 task 是此 parent 的 child：
   - `_deactivate_task(clear_session=False)`（清除 `.current-task`，**保留** `.current-session`）
   - 更新 child 的 `status` 为 `"completed"`，`completedAt` 为今天
3. 找下一个未完成的 child（`status not in ("completed", "done")`，见 D6）
4. 如果有 → `_activate_task(next_child)`（设 `.current-task`），返回 next 信息
5. 如果没有 → 返回 `all_done`，parent status → `completed`（见 D3）

**无 children 时逻辑：**
- `advance` **不写** `current_phase`（hook 独占，见 D1）
- 等价于 `next`：返回当前 phase 信息供 AI 决定调哪个 agent
- AI 调完 agent 后 hook 自动推进 phase，下次调 `next/advance` 即可看到新状态

**边界情况：**
- `.current-task` 不属于此 parent → exit 1 + stderr："Current task {x} is not a child of {parent}"（见 D5）
- 没有 `.current-task` → 直接激活第一个未完成的 child（容错：resume 场景）
- 路径比较使用 normalize（见 D2）
- 复用提取的 `_activate_task()`/`_deactivate_task()` helper（见 D7）
- Parent status 自动更新（见 D3）

**输出**：同 `next` 命令格式。

### R4: `task.py log <task-dir> <message> [--type TYPE]` — 结构化日志

追加一条记录到 task 目录下的 `run.log.jsonl`。

```jsonl
{"timestamp": "2026-03-10T14:30:00", "type": "decision", "message": "选择方案 A 因为更简单"}
{"timestamp": "2026-03-10T15:00:00", "type": "error", "message": "Lint failed on foo.ts:42"}
{"timestamp": "2026-03-10T15:30:00", "type": "note", "message": "Context compacted, resumed from s2-core"}
```

参数：
- `<task-dir>`: 任务目录（parent 或 child 均可）
- `<message>`: 日志内容（必填）
- `--type`: 日志类型，默认 `note`。可选值：`decision` | `error` | `note` | `compaction`

`status` 命令在输出末尾显示最近 3 条日志。

### R5: `.current-session` 平台感知

新增 `.trellis/.current-session` JSON 文件，记录当前 session 的平台信息。

**写入**：`task.py start --platform <name>`

```bash
$ python3 task.py start .trellis/tasks/03-10-s2-core --platform cursor
# 写 .current-task（不变）+ 写 .current-session（新增）
```

`--platform` 可选。不传时不写 `.current-session`。

**读取**：`next`/`advance` 输出时读 `.current-session` 的 `platform` 字段，决定输出 `execution` 和 `hint`。

**清除**：`task.py finish` 同时删除 `.current-task` 和 `.current-session`。

**Session-start hook 自动写入（Future Scope）**：Claude Code 和 iFlow 的 session-start hook **未来可以**在触发时自动写入
`.current-session`（`platform` 由 hook 文件路径推断：`.claude/hooks/` → `claude`，`.iflow/hooks/` → `iflow`）。
这样用户不需要手动传 `--platform`。

> ⚠️ 本版不修改 hooks（见 Non-Goals）。hook 自动写入的适配留给后续 task。
> 本版依赖 `task.py start --platform <name>` 手动传入（或不传，默认 subagent 模式）。

**`--platform` 验证**：只接受已知平台值（见下方 Platform 值约定表）。未知值 → exit 1 + stderr 错误。

**Stale `.current-session` 防护**：
- `task.py start` 在写 `.current-task` 前，检查是否已有 `.current-session` 且非本次写入
  - 如果有 → stderr 警告 "Stale .current-session detected, overwriting"，继续执行
- 这防止上次 session 异常退出后残留文件影响新 session

**gitignore 更新**：三个模板文件需要新增 `.current-session`：
- `.trellis/.gitignore`
- `packages/cli/src/templates/trellis/gitignore.txt`
- `packages/cli/src/templates/markdown/gitignore.txt`

## Acceptance Criteria

### 重构前提
- [ ] `_activate_task()`/`_deactivate_task()` helper 从 cmd_start/cmd_finish 提取（D7）
- [ ] 现有 `cmd_start`/`cmd_finish` 行为不变（回归测试）

### R1: status
- [ ] 有 children 时正确显示全局状态（含 current/next 标记）
- [ ] 无 children 时显示单任务状态
- [ ] 只读直接 children，不递归（D4）
- [ ] `--json` 输出纯 JSON，无 emoji（D5）
- [ ] 尾部显示最近 3 条 `run.log.jsonl` 日志

### R2: next
- [ ] 有 children 时返回正确的 child + action JSON
- [ ] 无 children 时返回自身 next_action 信息
- [ ] 所有完成时返回 `all_done`
- [ ] `completed` 和 `done` 都认为是完成（D6）
- [ ] 路径比较使用 normalize（D2）
- [ ] child dir 不存在时 stderr 警告 + 跳过（D5）

### R3: advance
- [ ] 有 children 时正确执行 finish→start 切换
- [ ] 复用 `_activate_task()`/`_deactivate_task()` + lifecycle hooks
- [ ] Parent status 自动转换：planning→in_progress→completed（D3）
- [ ] 无 children 时**不写** current_phase，只返回当前状态（D1）
- [ ] 无 .current-task 时容错激活第一个未完成 child
- [ ] .current-task 不属于 parent 时 exit 1 + 错误消息（D5）

### R4: log
- [ ] 追加 JSONL 记录到 `run.log.jsonl`
- [ ] 支持 --type flag（decision/error/note/compaction）

### R5: .current-session
- [ ] `task.py start --platform <name>` 写入 `.current-session` JSON
- [ ] `--platform` 只接受已知平台值，未知值 exit 1（D8 验证）
- [ ] `task.py finish` 清除 `.current-session`（`cmd_finish` 调 `_deactivate_task(clear_session=True)`）
- [ ] `advance` 内部 child 切换**不清除** `.current-session`（`_deactivate_task(clear_session=False)`，D8）
- [ ] `--platform` 不传时不写 `.current-session`（向后兼容）
- [ ] Stale `.current-session` 检测：`start` 时若已存在则 stderr 警告 + 覆盖
- [ ] `next`/`advance` 读 `.current-session` → 所有 action 类型都输出正确的 `execution` + `hint`（implement/check/finish/create-pr，见 D8 映射表）
- [ ] 无 `.current-session` 时默认 `execution: "subagent"`
- [ ] `.gitignore` 三个模板文件同步新增 `.current-session`
- [ ] Hook 自动写入**不在本版实现**（Non-Goals）

### 通用
- [ ] 所有命令在不适用的 task 上给出合理错误提示（exit code 见 D5）
- [ ] 向后兼容：不改变 task.json schema，不影响现有命令
- [ ] 单元测试覆盖核心逻辑

## Impact Analysis

### 直接受益

1. **trellis-autopilot skill** — TASK-PROMPT.md 从 ~80 行降到 ~5 行，PROGRESS.md 不再需要
2. **start.md** — Phase 3 (Execute) 从写死的 "Step 8→9→10" 简化为 "循环调 task.py next"
3. **session-start.py hook** — 可直接调 `task.py next` 把下一步指令注入 context
4. **dispatch.md** — 不再需要自己解析 next_action 数组

### 统一三个场景

```
普通开发 (start.md)    autopilot (新 session)    parallel (dispatch)
        │                      │                       │
        └──── 都用 task.py next/advance ──────────────┘
```

### 核心收益

- **抗 compaction**：状态在磁盘（task.json），不在 AI 上下文
- **prompt 精简**：AI 只需知道"调 task.py next"，不需要记住完整流程
- **可维护性**：改流程只需改 task.py 逻辑，不需要改多个 prompt/agent 定义

## Technical Notes

### 实现步骤（建议顺序）

1. **重构**：从 `cmd_start`/`cmd_finish` 提取 `_activate_task()`/`_deactivate_task()` helper（D7）
2. **paths.py**：新增 `.current-session` 的 get/set/clear 函数（D8）
3. **gitignore**：三个模板新增 `.current-session`（D8）
4. **start/finish 改造**：`cmd_start` 加 `--platform`；`cmd_finish` 清除 `.current-session`
5. **log**：最简单的新命令，独立实现
6. **status**：读取 + 显示，依赖 path normalize 逻辑
7. **next**：核心状态机查询，读 `.current-session` 决定 execution/hint
8. **advance**：最复杂，依赖 next + helper 函数 + parent status 更新

### 约束

- 四个命令 + session 机制在 `.trellis/scripts/task.py` 和 `common/paths.py` 中实现
- 读写现有 task.json + 新增 `run.log.jsonl` + 新增 `.current-session`
- `.current-task` 文件格式**不变**，现有 4 处读取代码**零改动**
- CLI npm 包只需更新 gitignore 模板和 paths.ts 常量
- 不需要改 hooks（hook 管 child 内部 phase，advance 管 parent 层 child 切换，见 D1）
- children 顺序由 parent task.json 的 `children[]` 数组决定
- 只支持 depth=1 直接 children（见 D4）
- 先只支持串行编排；未来可扩展 `depends_on` 支持并行

## Non-Goals (This Version)

- 并行子任务调度（`depends_on` 依赖图）
- 嵌套 children 递归编排（depth > 1，见 D4）
- 自动重试失败的 child
- `advance` 写 `current_phase`（hook 独占，见 D1）
- Hook 改造（session-start hook 自动写入 `.current-session`、inject-subagent-context 适配留给后续 task）
- start.md / dispatch.md 的 prompt 重写（留给后续 task）
- Worktree 模式下的 task.json 双副本同步（留给 S4 worktree task）

## Related

- **trellis-autopilot skill**: `marketplace/skills/trellis-autopilot/` — 第一个受益的消费方
- **v0.4.0-beta.1**: 可作为 v0.4.0 的独立子任务
- **S2 命令合并**: `03-10-s2-commands/` — start.md 已在该 task 中更新，后续可复用 next/advance
