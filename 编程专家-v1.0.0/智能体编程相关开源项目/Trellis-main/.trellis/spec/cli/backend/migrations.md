# Migration System

智能迁移系统，用于处理模板文件重命名和删除。

## 目录结构

```
src/migrations/
├── index.ts              # 迁移逻辑 (动态加载 JSON)
└── manifests/
    └── {version}.json    # 各版本迁移清单
```

## 添加新版本迁移

创建 `src/migrations/manifests/{version}.json`：

```json
{
  "version": "0.2.0",
  "description": "变更说明",
  "migrations": [
    {
      "type": "rename",
      "from": ".claude/commands/old.md",
      "to": ".claude/commands/new.md",
      "description": "重命名原因"
    },
    {
      "type": "delete",
      "from": ".trellis/scripts/deprecated.py",
      "description": "删除原因"
    }
  ]
}
```

**无需修改任何代码** - 构建时自动复制到 dist。

## 迁移类型

| Type | 必填字段 | 说明 |
|------|----------|------|
| `rename` | `from`, `to` | 重命名文件 |
| `rename-dir` | `from`, `to` | 重命名目录（包含所有子文件） |
| `delete` | `from` | 删除文件 |
| `safe-file-delete` | `from`, `allowed_hashes` | Hash 校验后自动删除废弃文件（无需 `--migrate`） |

### rename-dir 示例

```json
{
  "type": "rename-dir",
  "from": ".trellis/structure",
  "to": ".trellis/spec",
  "description": "重命名 structure 为 spec"
}
```

**特点**：
- 整个目录移动（包括用户添加的文件）
- 自动批量更新 hash 追踪
- 移动后自动清理空的源目录
- 嵌套目录按深度优先处理（避免父目录先移动导致子目录找不到）

### safe-file-delete 示例

```json
{
  "type": "safe-file-delete",
  "from": ".claude/commands/trellis/before-backend-dev.md",
  "description": "Replaced by before-dev.md",
  "allowed_hashes": ["7e35444de2a5779ef39944f17f566ea21d2ed7f4994246f4cfe6ebf9a11dd3e3"]
}
```

**工作机制**：
- **无需 `--migrate`** — 在每次 `trellis update` 时自动执行
- **Hash 校验** — 只有当文件内容的 SHA256 匹配 `allowed_hashes` 中的某个值时才删除
- **版本无关** — 从所有 manifest 收集 safe-file-delete 条目，不受版本范围限制
- 删除后自动清理 hash 记录和空目录

**分类逻辑**：

| 分类 | 条件 | 行为 |
|------|------|------|
| `delete` | 文件存在，hash 匹配，非 protected，非 update.skip | 删除文件 |
| `skip-missing` | 文件不存在 | 跳过 |
| `skip-modified` | 文件存在但 hash 不匹配（用户已修改） | 保留 |
| `skip-protected` | 路径在 PROTECTED_PATHS 中 | 保留 |
| `skip-update-skip` | 路径在 config.yaml `update.skip` 中 | 保留 |

## 分类逻辑

| 分类 | 条件 | 行为 |
|------|------|------|
| `auto` | 文件未被用户修改 / rename-dir | 自动迁移 |
| `confirm` | 文件已被用户修改 | 默认询问，`-f` 强制，`-s` 跳过 |
| `conflict` | 新旧路径都存在 | 跳过并提示手动解决 |
| `skip` | 旧路径不存在 / 路径受保护 | 无需操作 |

## 受保护路径

以下路径不会被任何迁移操作修改或删除（用户数据）：

- `.trellis/workspace` — 开发者工作记录
- `.trellis/tasks` — 任务追踪
- `.trellis/spec` — 开发指南（用户自定义）
- `.trellis/.developer` — 开发者身份
- `.trellis/.current-task` — 当前任务指针

> 注意：`rename`/`rename-dir` 类型允许将文件迁移 **到** 受保护路径（例如 0.2.0 的 `agent-traces` → `workspace` 重命名），但不允许从受保护路径迁移。

## update.skip 配置

在 `config.yaml` 中配置跳过路径，防止 safe-file-delete 删除指定文件：

```yaml
update:
  skip:
    - .claude/commands/trellis/my-custom.md
    - .cursor/commands/
```

- 支持文件路径和目录路径（目录路径以 `/` 结尾，匹配所有子文件）
- 同时影响模板更新和 safe-file-delete

## 模板哈希追踪

- 存储位置：`.trellis/.template-hashes.json`
- 用途：检测用户是否修改过模板文件
- 原理：比较当前文件 SHA256 与存储的哈希值
- 初始化：`trellis init` 时自动创建
- 更新：`trellis update` 后自动更新被覆盖文件的哈希

## CLI 使用

```bash
trellis update              # 显示迁移提示
trellis update --migrate    # 执行迁移（修改过的文件会提示确认）
trellis update --migrate -f # 强制迁移（备份后执行）
trellis update --migrate -s # 跳过修改过的文件
```

## 相关文件

- `src/types/migration.ts` - 类型定义
- `src/migrations/index.ts` - 迁移逻辑
- `src/utils/template-hash.ts` - 哈希工具
- `src/commands/update.ts` - 更新命令集成
