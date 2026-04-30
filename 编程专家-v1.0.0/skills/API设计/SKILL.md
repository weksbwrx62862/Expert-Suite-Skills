---
name: API设计
description: >
  根据业务需求设计RESTful或GraphQL API接口，包含URL规范、请求响应格式、错误码设计和版本控制策略。
  触发词："API设计"、"接口设计"、"设计API"、"RESTful"、"GraphQL"、
  "怎么设计接口"、"API规范"、"接口文档"、"设计REST接口"、
  "API最佳实践"、"接口规范"、"怎么定义API"。
argument-hint: "描述业务需求+数据模型+接口类型偏好"
name_en: "api-design"
description_en: >
  Design RESTful or GraphQL APIs based on business requirements, including URL conventions,
  request/response formats, error codes, and versioning strategy.
  Trigger phrases: "design API", "API design", "RESTful API", "GraphQL",
  "interface design", "API specification", "endpoint design", "API best practices".
---

# /API设计 -- 智能API设计

> 如遇到不熟悉的占位符，参见 [CONNECTORS.md](../../CONNECTORS.md)。

**独立能力（无需连接器）**

- 设计RESTful/GraphQL API接口
- 定义请求响应格式和字段规范
- 设计错误码和状态码体系
- 生成OpenAPI/Swagger规范文档

**增强能力（连接器加持）**

- ~~Filesystem → 读取现有API代码，保持风格一致性

## 连接器（可选增强）

| 连接器 | 增强能力 |
|--------|---------|
| **~~Filesystem** | 读取现有API代码，保持接口风格一致性 |

> 没有连接器也完全可以使用——基于通用RESTful/GraphQL最佳实践设计。

## 调用方式

```
/API设计 <业务需求>
```

设计以下业务的API：@$1

## 输入要求

1. **业务需求**（必填）：需要设计的业务场景和功能
2. **数据模型**（必填）：核心实体和字段
3. **接口类型**（可选）：RESTful或GraphQL，默认RESTful
4. **已有接口**（可选）：如果已有部分接口需要兼容
5. **特殊要求**（可选）：如"需要支持批量操作"、"需要Webhook回调"

## 执行流程

### 第一步：需求分析

- 识别API的使用场景和用户
- 确定API的功能边界
- 明确输入输出数据模型

### 第二步：设计原则应用

- 应用RESTful或GraphQL设计原则
- 设计URL结构和HTTP方法
- 定义请求/响应格式

### 第三步：详细设计

- 设计每个端点的详细规范
- 定义错误处理策略
- 设计认证和授权机制

### 第四步：Spec Artifact输出（Harness增强）

API设计完成后输出为spec artifact，供后续任务引用：

```markdown
## API Spec: [API名称]

### ADDED Requirements

#### Requirement: [端点名称]
The system SHALL provide an endpoint to [功能描述].

##### Scenario: 成功请求
- GIVEN [前置条件]
- WHEN 发送 `[METHOD] [路径]` 请求
- THEN 返回 [状态码] 和 [响应体]

##### Scenario: 错误处理
- GIVEN [错误前置条件]
- WHEN 发送 `[METHOD] [路径]` 请求
- THEN 返回 [错误状态码] 和 [错误响应体]

### Design
- **URL结构**: [结构说明]
- **认证方式**: [认证机制]
- **版本策略**: [版本管理]

### File Changes
- `[API定义文件]` (new/modified)
```

**提示用户**：此spec artifact可被 `/代码生成` 和 `/测试用例生成` 引用。

### 第五步：文档生成

- 生成OpenAPI/Swagger规范
- 编写使用示例
- 提供SDK代码示例

## 输出格式

```
## API设计文档

### 资源定义

| 资源 | 说明 | 核心字段 |
|------|------|---------|
| [资源名] | [说明] | [字段列表] |

### 接口列表

#### [接口名称]

**URL**：`[METHOD] /path`
**说明**：[功能说明]

**请求参数**：
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| [字段] | [类型] | [是/否] | [说明] |

**响应格式**：
```json
{
  "code": 0,
  "data": { ... },
  "message": "success"
}
```

**错误码**：
| 错误码 | 说明 |
|--------|------|
| [CODE] | [说明] |

### 通用规范

- **认证方式**：[Bearer Token / API Key / OAuth2]
- **版本控制**：[URL路径 / Header / 参数]
- **分页方式**：[页码分页 / 游标分页]
- **数据格式**：[snake_case / camelCase]
```

## 质量标准

- URL必须使用名词复数形式，不能用动词（如/users而非/getUsers）
- HTTP方法必须符合语义（GET无副作用、POST创建、PUT幂等更新、DELETE删除）
- 错误响应必须包含机器可读的错误码和人工可读的消息
- 分页接口必须说明最大页大小和默认页大小
- 敏感操作（删除、批量修改）必须要求二次确认或特殊权限
- 不得设计返回超大列表的接口（必须分页或流式）

## 关联Skill

- **技术选型** — 设计前可用 `/技术选型` 确定API技术方案（REST/GraphQL/gRPC）
- **代码生成** — 设计后可用 `/代码生成` 生成API接口代码
- **测试用例生成** — 设计后可用 `/测试用例生成` 生成API测试
- **文档生成** — 设计后可用 `/文档生成` 生成API文档
