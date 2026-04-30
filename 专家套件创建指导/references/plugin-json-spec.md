# plugin.json 规范

## 完整字段说明

```json
{
  "name": "套件英文标识",
  "displayName": "套件中文展示名",
  "version": "1.1.1",
  "description": "一句话描述套件功能和覆盖场景",
  "author": {
    "name": "作者名称"
  },
  "keywords": [
    "关键词1",
    "关键词2",
    "关键词3"
  ],
  "skills": [
    "Skill名称1",
    "Skill名称2",
    "Skill名称3"
  ],
  "displayNameEn": "English Display Name",
  "descriptionEn": "English description of the suite"
}
```

## 字段详解

### name（必填）

- 类型：string
- 格式：kebab-case（短横线连接的小写字母）
- 示例：`equity-research`、`contract-management`、`hr-recruitment`
- 规则：
  - 只能包含小写字母、数字和短横线
  - 不能以数字开头
  - 不能包含空格或下划线

### displayName（必填）

- 类型：string
- 示例：`投研分析`、`合同管理`、`HR招聘`
- 规则：
  - 使用岗位或领域常用名称
  - 简洁明了，不超过8个汉字

### version（必填）

- 类型：string
- 格式：semver（主版本.次版本.修订号）
- 示例：`1.0.0`、`1.1.1`、`2.0.0`
- 版本升级规则：
  - 修订号（Z）：Bug修复、文案优化
  - 次版本号（Y）：新增Skill、功能增强
  - 主版本号（X）：重大架构调整、不兼容变更

### description（必填）

- 类型：string
- 长度：50-150字
- 内容：覆盖场景 + 核心价值
- 示例：
  - 好：`券商/基金投研全流程工具，覆盖深度报告、行业研究、年报解读、业绩快评、调研纪要、晨会纪要和研报摘要七大场景。`
  - 差：`这是一个投研工具。`

### author（必填）

- 类型：object
- 结构：`{"name": "作者名称"}`
- 示例：`{"name": "QoderWork"}` 或 `{"name": "阿里云法务部"}`

### keywords（必填）

- 类型：string[]
- 数量：5-15个
- 内容：岗位关键词 + 场景关键词 + 工具关键词
- 示例（投研分析）：
  ```json
  [
    "金融",
    "投研",
    "研报",
    "行业研究",
    "年报",
    "调研",
    "晨会",
    "业绩快评",
    "估值",
    "券商",
    "深度报告",
    "可比公司",
    "估值对比"
  ]
  ```

### skills（必填）

- 类型：string[]
- 数量：5-10个
- 内容：与 skills/ 文件夹下的子文件夹名称完全一致
- 示例：
  ```json
  [
    "深度报告",
    "行业研究",
    "读年报",
    "业绩快评",
    "调研纪要",
    "晨会纪要",
    "研报摘要",
    "可比公司分析"
  ]
  ```
- 注意：名称必须与文件夹名一致，否则会导致Skill无法加载

### displayNameEn（可选）

- 类型：string
- 示例：`Equity Research`、`Contract Management`

### descriptionEn（可选）

- 类型：string
- 长度：50-200字
- 示例：
  ```
  End-to-end equity research toolkit for sell-side and buy-side analysts,
  covering deep-dive reports, industry research, annual report analysis,
  earnings reviews, field research notes, morning briefings, and research digests.
  ```

## 验证清单

| 检查项 | 验证方法 |
|--------|---------|
| [ ] `name` 符合 kebab-case | 检查是否只包含小写字母、数字和短横线 |
| [ ] `version` 符合 semver | 检查格式是否为X.Y.Z |
| [ ] `skills` 数组与文件夹名称完全一致 | 逐项比对skills数组和skills/下的文件夹名 |
| [ ] `description` 超过50字 | 统计字符数 |
| [ ] `keywords` 包含至少5个词 | 数keywords数组长度 |
| [ ] 所有必填字段已填写 | 检查name、displayName、version、description、author、keywords、skills |
| [ ] JSON格式有效 | 使用JSON解析器验证 |

## 常见错误

| 错误 | 表现 | 验证方法 | 修正 |
|------|------|---------|------|
| skills数组与文件夹不一致 | plugin.json中"深度报告"，文件夹是"深度研报" | 逐项比对 | 统一名称 |
| 版本号格式错误 | "v1.0" 或 "1.0"（缺少修订号） | 检查是否为X.Y.Z | 改为"1.0.0" |
| description过短 | "这是一个投研工具"（<50字） | 统计字符数 | 补充覆盖场景 |
| name含大写字母 | "EquityResearch" | 检查是否全小写 | 改为"equity-research" |
