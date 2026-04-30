---
name: 专家套件创建指导
description: >
  指导用户将岗位专业知识封装为QoderWork专家套件。覆盖套件架构设计、Skill编写、连接器配置、plugin.json定义和README撰写全流程。
  当用户说"创建专家套件"、"封装专家套件"、"做一个套件"、"怎么打包技能"、"制作专家套件"、
  "写plugin.json"、"配置连接器"、"设计Skill"、"封装岗位能力"、"做技能包"时触发。
  也用于已有套件的迭代优化和新增Skill的场景。
argument-hint: "描述要封装的岗位领域和核心能力，例如：封装一个HR招聘套件，包含简历筛选、面试评估、Offer谈判三个技能"
name_en: "expert-suite-creation-guide"
description_en: >
  Guide users to package domain expertise into QoderWork expert suites. Covers suite architecture design,
  Skill authoring, connector configuration, plugin.json definition, and README writing.
  Trigger when user says "create expert suite", "package expert suite", "build a suite", "how to bundle skills",
  "make expert suite", "write plugin.json", "configure connectors", "design Skill", "package role capabilities",
  or "create skill pack".
---

# 专家套件创建指导

将岗位专业知识封装为可一键安装、开箱即用的专家套件。

## 核心概念

专家套件 = 岗位能力包。封装一个岗位的完整工作体系——流程、标准、工具连接、输出规范。

三层架构：
- **连接器**：解决"AI能用什么工具"
- **技能（Skill）**：解决"活儿怎么干"，把SOP固化为可复用知识单元
- **专家套件**：多个技能 + 所需连接器打包成面向特定岗位的完整能力包

## 创建流程

```
岗位分析 → Skill设计 → 资源准备 → 文件编写 → 打包验证
```

### Step 1: 岗位分析

回答五个问题确定套件定位：

| 问题 | 示例 |
|------|------|
| 面向什么岗位？ | 券商研究员/基金经理 |
| 解决什么核心问题？ | 研究报告撰写效率低 |
| 日常工作有哪些高频场景？ | 深度报告、业绩快评、调研纪要 |
| 需要连接哪些工具？ | Notion（知识库沉淀） |
| 输出物是什么格式？ | Markdown研报、纪要模板 |

梳理5-10个Skill，覆盖岗位核心工作流。命名用"动词+名词"，如"审查合同"、"业绩快评"。

### Step 2: Skill设计

每个Skill是一个独立文件夹：

```
Skill名称/
├── SKILL.md              # 必需
├── references/           # 可选：参考文档
├── scripts/              # 可选：可执行脚本
└── assets/               # 可选：模板资源
```

SKILL.md 标准结构：

```markdown
---
name: Skill名称
description: >
  一句话说明功能。触发词："词1"、"词2"、"词3"。
argument-hint: "输入提示"
name_en: "english-name"
description_en: >
  English description. Trigger phrases: "phrase1", "phrase2".
---

# /Skill名称 -- 功能标题

**独立能力（无需连接器）**
- 能力1
- 能力2

**增强能力（连接器加持）**
- ~~ConnectorName → 增强效果

## 连接器（可选增强）

| 连接器 | 增强能力 |
|--------|---------|
| **~~ConnectorName** | 增强效果描述 |

> 没有连接器也完全可以使用——说明无连接器时的工作方式。

## 调用方式

```
/Skill名称 <参数>
```

处理：@$1

## 输入要求

1. **必填项1**：说明
2. **选填项1**（可选）：说明

## 执行流程

### 第一步：XXX
- 子步骤
- 子步骤

### 第二步：XXX
| 条件 | 处理方式 |
|------|---------|
| A | 处理A |
| B | 处理B |

## 输出格式

```
## 输出标题
**字段**：[值]
...
```

## 质量标准

- 要求1：具体标准
- 要求2：具体标准

## 关联Skill

- **Skill名** -- 衔接场景
```

**关键规则**：
- description 必须包含触发词（至少3个同义表达）
- 所有Skill在无连接器时必须能独立运行
- 执行流程按步骤编号，复杂判断用表格
- 输出格式提供完整模板，含占位符说明
- 质量标准可验证，包含红线规则

**References 使用原则**：

| 放SKILL.md | 放references/ |
|-----------|--------------|
| 核心工作流程 | 详细格式规范 |
| 触发条件 | 市场数据区间 |
| 输出模板 | 长篇幅参考文档 |
| 质量标准 | 脚本和模板文件 |

参见 [skill-template.md](references/skill-template.md) 获取完整模板和字段说明。
参见 [trigger-design-guide.md](references/trigger-design-guide.md) 获取触发词设计标准。

### Step 3: 套件级文件

#### plugin.json

路径：`.qoder-plugin/plugin.json`

```json
{
  "name": "kebab-case-id",
  "displayName": "中文名",
  "version": "1.1.1",
  "description": "一句话描述覆盖场景",
  "author": { "name": "QoderWork" },
  "keywords": ["词1", "词2"],
  "skills": ["Skill名称1", "Skill名称2"],
  "displayNameEn": "English Name",
  "descriptionEn": "English description"
}
```

规则：`skills` 数组与文件夹名称完全一致；`name` 用 kebab-case。

参见 [plugin-json-spec.md](references/plugin-json-spec.md) 获取完整字段规范。

#### .mcp.json

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

规则：连接器是可选增强，不是必需。用 `~~ConnectorName` 作为占位符。

参见 [mcp-config-guide.md](references/mcp-config-guide.md) 获取配置详情。

#### CONNECTORS.md

必须说明：占位符使用方式、无连接器时的工作方式、安装连接器后的增强效果。

#### README.md

必须包含：能力层级图（ASCII）、适用角色、Skill工作流图、快捷命令表格、MCP增强说明。

参见 [readme-template.md](references/readme-template.md) 获取完整模板。

### Step 4: 目录结构

```
套件名称-v1.1.1/
├── .qoder-plugin/
│   └── plugin.json
├── .mcp.json
├── CONNECTORS.md
├── README.md
├── README_EN.md
└── skills/
    ├── Skill名称1/
    │   ├── SKILL.md
    │   ├── references/
    │   ├── scripts/
    │   └── assets/
    └── Skill名称2/
        └── SKILL.md
```

### Step 5: 质量检查

| 检查项 | 验证方法 |
|--------|---------|
| SKILL.md frontmatter完整 | 检查name + description |
| description含触发词 | 列出至少3个同义表达 |
| 无连接器可独立运行 | 检查"独立能力"section |
| 执行流程步骤清晰 | 每步有明确输入和输出 |
| 输出模板完整 | 所有占位符有填充逻辑 |
| plugin.json skills与文件夹一致 | 逐项比对 |
| 版本号符合semver | 格式：X.Y.Z |

完整检查清单参见 [quality-checklist.md](references/quality-checklist.md)。

## 设计原则

- **简洁优先**：SKILL.md < 500行，核心流程在references
- **工具无关**：用 `~~ConnectorName` 占位符，不绑定具体产品
- **渐进增强**：连接器只增加便利性，不增加核心功能
- **可验证质量**：每条质量标准都有具体的yes/no检查方法

## 迭代与错误排查

迭代节奏：首次封装（3-5个核心场景）→ 使用验证（1-2周）→ 补充完善 → 版本更新。

常见错误：Skill过大（拆分为独立Skill）、触发词缺失（补充同义表达）、连接器依赖（设计独立能力）、输出不规范（提供完整模板）。

参见 [iteration-guide.md](references/iteration-guide.md) 和 [common-mistakes.md](references/common-mistakes.md)。

## 示例

从0创建"HR招聘套件"的完整示例参见 [examples/hr-recruitment-suite.md](references/examples/hr-recruitment-suite.md)。
