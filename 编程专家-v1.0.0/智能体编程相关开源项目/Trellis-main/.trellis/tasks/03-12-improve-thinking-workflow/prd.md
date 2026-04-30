# 改善 Brainstorm/Break-Loop 流程：集成思考指南

## Background

当前 `brainstorm` 和 `break-loop` 是独立的 slash command，各自有固定的流程模板。
但缺少与 `spec/guides/` 中思考指南的联动——brainstorm 时不会参考历史思考模式，
break-loop 产出的洞察也只是在当次对话中更新 spec，没有形成可复用的思考框架。

## Goal

让 brainstorm 和 break-loop 形成闭环：
1. **Brainstorm 时**：自动读取 `spec/guides/` 中的思考指南，基于历史经验提问
2. **Break-loop 后**：将洞察沉淀为可复用的思考模式（不只是 spec 条目）

## Requirements

### 1. Brainstorm 集成思考指南

- [ ] `brainstorm` 命令开始时，读取 `spec/guides/index.md` 获取可用指南列表
- [ ] 根据任务类型（backend/frontend/fullstack/scripts）自动推荐相关指南
- [ ] 提问时参考指南中的 "Thinking Triggers" checklist
- [ ] 在 PRD 生成时，附带引用了哪些思考指南

### 2. Break-loop 洞察沉淀

- [ ] Break-loop 分析后，检查是否有通用的思考模式可提取
- [ ] 通用模式写入 `spec/guides/` 中对应的指南文件（现有行为，保持）
- [ ] 新增：如果发现全新的思考维度，创建新的 thinking guide 文件
- [ ] 更新 `spec/guides/index.md` 注册新指南

### 3. 新增思考指南文件

基于 Codex review 的经验，考虑新增：

- [ ] `ai-review-thinking-guide.md` — AI 交叉审查的验证方法论
  - 信任边界判断（内部数据 vs 外部输入）
  - 设计意图识别（代码注释 vs bug）
  - 假阳性过滤 checklist
  - 测试有效性验证（心理删除测试）

### 4. 命令更新

- [ ] 更新 `brainstorm` 命令模板，加入读取 guides 的步骤
- [ ] 更新 `break-loop` 命令模板，加入思考模式提取步骤
- [ ] 各平台同步更新（claude/iflow/cursor/codex/kiro/gemini/kilo/opencode/qoder）

## Technical Notes

- 思考指南存放在 `.trellis/spec/guides/`，随项目版本管理
- 命令模板在 `packages/cli/src/templates/` 下各平台目录中
- 指南文件格式已有先例：`code-reuse-thinking-guide.md`、`cross-layer-thinking-guide.md` 等

## Acceptance Criteria

- [ ] Brainstorm 开始时能看到相关思考指南的引用
- [ ] Break-loop 分析后能判断是否需要创建新指南
- [ ] 至少新增 1 个思考指南文件（ai-review-thinking-guide.md）
- [ ] 命令模板在所有平台同步
