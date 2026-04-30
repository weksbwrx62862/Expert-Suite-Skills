# MCP 连接器配置指南

## 基本概念

MCP（Model Context Protocol）是AI与外部工具通信的标准协议。专家套件通过MCP连接企业内部工具（Notion、飞书、邮件、CRM等）。

**核心原则**：连接器是可选增强，不是必需。所有Skill必须能在无连接器时独立工作。

## .mcp.json 格式

```json
{
  "mcpServers": {
    "服务标识": {
      "type": "http",
      "url": "https://mcp.example.com/mcp"
    },
    "另一个服务": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
    }
  }
}
```

## 支持的连接器类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `http` | HTTP/SSE 连接 | 云端SaaS服务（Notion、飞书等） |
| `stdio` | 标准输入输出 | 本地工具、命令行程序 |

## 常见连接器配置示例

### Notion

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

### 飞书

```json
{
  "mcpServers": {
    "feishu": {
      "type": "http",
      "url": "https://mcp.feishu.cn/mcp"
    }
  }
}
```

### 本地文件系统

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

## SKILL.md 中的连接器引用

使用 `~~服务名` 作为占位符：

```markdown
**增强能力（连接器加持）**
- ~~Notion → 将报告写入Notion知识库

## 连接器（可选增强）

| 连接器 | 增强能力 |
|--------|---------|
| **~~Notion** | 将生成的报告写入Notion知识库 |

> 没有连接器也完全可以使用——基于内置知识完成核心功能。

**如已连接 ~~Notion：**
- 询问用户是否需要将报告写入Notion
```

## 占位符命名规范

| 服务 | 占位符 | 说明 |
|------|--------|------|
| Notion | `~~Notion` | 知识库、文档协作 |
| 飞书 | `~~Feishu` | 文档、表格、消息 |
| 邮件 | `~~Email` | 邮件发送、收件箱 |
| 日历 | `~~Calendar` | 日程管理、会议安排 |
| CRM | `~~CRM` | 客户管理、商机跟踪 |
| 设计工具 | `~~设计工具` | Figma等设计协作 |

## CONNECTORS.md 模板

```markdown
# Connectors

## 占位符说明

插件文件中使用 `~~Notion` 作为工具占位符，代表 Notion MCP 服务。

插件是工具无关的——用类别描述工作流，而非特定产品。`.mcp.json` 预配置了 Notion MCP 服务。

## 本插件的连接器

| 类别 | 占位符 | 已配置服务 | 增强能力 | 状态 |
|------|--------|-----------|---------|------|
| Notion | `~~Notion` | Notion MCP（notion） | 将生成的报告写入Notion知识库 | 可选 |

## 无连接器时的工作方式

- 数据 → 从用户上传的文件中提取
- 输出 → 以对话形式输出，用户手动复制到目标平台

## 安装连接器后的增强

| 连接器 | 受益最大的Skill | 增强效果 |
|--------|----------------|---------|
| `~~Notion` | 全部Skill | 报告写入Notion，便于团队协作和知识沉淀 |
```

## 设计原则

1. **工具无关性**：用 `~~Notion` 而不是 `~~具体产品名`，保持抽象层级
2. **可选增强**：所有Skill在无连接器时必须有完整的独立工作能力
3. **渐进增强**：连接器只增加便利性，不增加核心功能
4. **清晰标注**：在Skill中明确标注哪些能力是"独立"的，哪些是"增强"的
