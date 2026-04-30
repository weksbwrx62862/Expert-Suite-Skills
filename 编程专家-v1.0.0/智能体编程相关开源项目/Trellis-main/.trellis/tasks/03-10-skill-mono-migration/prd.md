# Skill: 单仓迁移 Monorepo 指南

## Goal

创建一个 Trellis skill，引导用户将已有的单仓 `.trellis/` 项目迁移到 monorepo 模式。基于 Trellis 自身从单仓迁移到 monorepo（pnpm workspaces + git submodules）的实际经验总结。

## Background

- Trellis 主仓库自身经历了完整的单仓 → monorepo 迁移
- 相关归档 task 可作为经验来源：
  - `archive/2026-03/03-09-monorepo-submodule/` — Git submodule 设置
  - `archive/2026-03/03-09-monorepo-spec-adapt/` — Spec 目录重组（10 Part 蓝图）
  - `archive/2026-03/03-10-dogfood-monorepo-compat/` — Dotfile 适配
  - `archive/2026-03/03-10-merge-monorepo-branch/` — 分支合并
- 迁移涉及：spec 目录重组、dotfile 路径更新、config.yaml 配置、命令泛化等

## Scope

- 从上述归档 task 和 journal 记录中提取迁移步骤
- 编写为 skill（交互式引导 AI 完成迁移）
- 覆盖：spec 目录移动、config.yaml packages 配置、dotfile 路径更新、验证检查

## Priority

P3 — 在 v0.4.0 monorepo 支持完成后再做

## Dependencies

- S1 (config 基础设施) 完成
- S2 (命令动态化) 完成
