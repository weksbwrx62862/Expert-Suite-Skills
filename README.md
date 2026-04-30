<div align="center">

# 🛠️ 专家 SKILL 集合

**Trae IDE 专业技能插件集合 — 覆盖编程、写作、文档、安全、法律五大领域**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/weksbwrx62862/Expert-Suite-Skills?style=social)](https://github.com/weksbwrx62862/Expert-Suite-Skills)
[![Last Commit](https://img.shields.io/github/last-commit/weksbwrx62862/Expert-Suite-Skills)](https://github.com/weksbwrx62862/Expert-Suite-Skills)
[![Repo Size](https://img.shields.io/github/repo-size/weksbwrx62862/Expert-Suite-Skills)](https://github.com/weksbwrx62862/Expert-Suite-Skills)

</div>

---

> **让 AI 成为你的专业伙伴** — 专家 SKILL 集合将行业最佳实践封装为可一键调用的 AI 技能，无论是代码审查、文档生成还是合规检查，都能获得专家级的输出质量。

## 核心能力

| 领域 | 代号 | 技能数量 | 核心能力 | 适用场景 |
|:-----|:-----|:--------:|:---------|:---------|
| **编程相关** | `01-Programming` | 12 | 前端设计、代码审查、测试驱动开发、MCP 服务器构建 | 软件开发全流程 |
| **写作与语言** | `02-Writing` | 6 | 算法艺术、品牌指南、Canvas 设计、主题工厂 | 创意设计与内容创作 |
| **文档与幻灯片** | `03-Documents` | 5 | 文档协作、DOCX/PDF/PPTX/XLSX 处理 | 企业文档自动化 |
| **安全与法律** | `04-Compliance` | 1 | 合规检查、风险评估 | 法务与合规审查 |
| **系统与集成** | `05-System` | 3 | MCP 构建器、技能创建、系统架构 | 平台扩展与定制 |

## 架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Expert Suite Skills                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  01-编程相关  │  │ 02-写作与语言 │  │ 03-文档与幻灯片│              │
│  │  Programming │  │   Writing    │  │  Documents   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                       │
│         ▼                 ▼                 ▼                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Trae IDE Integration                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                 │                 │                       │
│         ▼                 ▼                 ▼                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ 04-安全与法律 │  │ 05-系统与集成 │  │  专家套件创建  │              │
│  │  Compliance  │  │    System    │  │   指导指南    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 快速开始

### 前置条件

- [Trae IDE](https://www.trae.ai/) 已安装
- Python 3.8+ 环境
- Git 客户端

### 安装配置

```bash
# 1. 克隆仓库
git clone https://github.com/weksbwrx62862/Expert-Suite-Skills.git

# 2. 进入项目目录
cd Expert-Suite-Skills

# 3. 将技能目录复制到 Trae IDE 的 Skills 目录
# Windows: %APPDATA%\Trae\Skills\
# macOS:   ~/Library/Application Support/Trae/Skills/
# Linux:   ~/.config/trae/skills/
```

### 最小示例

```python
# 在 Trae IDE 中使用编程技能
# 输入 / 唤起技能菜单，选择 "代码审查"

@skill("代码审查")
def review_code(code: str) -> str:
    """
    对输入的代码进行全面审查
    - 检查代码风格和规范
    - 识别潜在的 Bug 和安全漏洞
    - 提供重构建议
    """
    pass
```

## 技能详解

### 01-编程相关 (Programming)

| 技能名称 | 功能描述 | 触发词 | 输出格式 |
|:---------|:---------|:------|:---------|
| `代码审查` | 全面审查代码质量、风格和安全性 | `审查代码`, `review` | 详细报告 |
| `代码生成` | 根据需求自动生成代码实现 | `生成代码`, `generate` | 可执行代码 |
| `Bug诊断` | 分析错误日志，定位问题根源 | `诊断bug`, `debug` | 诊断报告 |
| `重构建议` | 提供代码重构方案和最佳实践 | `重构`, `refactor` | 改进方案 |
| `技术选型` | 评估和推荐技术栈方案 | `技术选型`, `tech stack` | 对比分析 |
| `API设计` | 设计 RESTful/GraphQL API | `设计API`, `api design` | API 规范 |
| `测试用例生成` | 自动生成单元测试和集成测试 | `生成测试`, `test gen` | 测试代码 |
| `文档生成` | 自动生成代码文档和 API 文档 | `生成文档`, `doc gen` | Markdown |
| `前端设计` | 创建响应式 UI 组件和布局 | `前端设计`, `frontend` | HTML/CSS |
| `测试驱动开发` | 实现 TDD 工作流和测试策略 | `TDD`, `测试驱动` | 测试套件 |
| `Git工作树` | 管理 Git 分支和工作树 | `git工作树`, `worktree` | 操作指南 |
| `MCP服务器构建` | 构建 Model Context Protocol 服务器 | `构建MCP`, `mcp server` | 服务器代码 |

### 02-写作与语言 (Writing)

| 技能名称 | 功能描述 | 触发词 | 输出格式 |
|:---------|:---------|:------|:---------|
| `算法艺术` | 使用 p5.js 创建生成艺术 | `算法艺术`, `generative` | p5.js 代码 |
| `品牌指南` | 应用品牌色彩和排版规范 | `品牌指南`, `brand` | 样式配置 |
| `Canvas设计` | 创建静态视觉设计和海报 | `设计`, `canvas` | 设计文件 |
| `前端设计(高级)` | 高保真前端界面实现 | `高级前端`, `premium` | 完整组件 |
| `主题工厂` | 生成和应用视觉主题 | `主题`, `theme` | 主题配置 |
| `网络小说创作` | 辅助网络小说写作和情节设计 | `小说`, `novel` | 章节内容 |

### 03-文档与幻灯片 (Documents)

| 技能名称 | 功能描述 | 触发词 | 输出格式 |
|:---------|:---------|:------|:---------|
| `文档协作` | 多人协作编辑和版本管理 | `协作`, `collab` | 协作文档 |
| `DOCX处理` | 创建和编辑 Word 文档 | `word`, `docx` | .docx 文件 |
| `PDF处理` | 提取和生成 PDF 文档 | `pdf`, `pdf处理` | .pdf 文件 |
| `PPTX处理` | 创建和编辑演示文稿 | `演示`, `pptx` | .pptx 文件 |
| `XLSX处理` | 处理电子表格和数据分析 | `表格`, `xlsx` | .xlsx 文件 |

### 04-安全与法律 (Compliance)

| 技能名称 | 功能描述 | 触发词 | 输出格式 |
|:---------|:---------|:------|:---------|
| `合规检查` | 检查代码和文档的合规性 | `合规`, `compliance` | 合规报告 |

**使用示例：**
```markdown
/compliance check --standard GDPR --scope data-processing

# 输出：
# 合规检查报告
# 标准: GDPR
# 范围: data-processing
# 状态: ⚠️ 需要改进
# 发现: 3 项潜在合规风险
```

### 05-系统与集成 (System)

| 技能名称 | 功能描述 | 触发词 | 输出格式 |
|:---------|:---------|:------|:---------|
| `MCP构建器` | 构建自定义 MCP 服务器 | `构建MCP`, `mcp builder` | 服务器框架 |
| `技能创建` | 创建新的 Trae IDE 技能 | `创建技能`, `skill create` | 技能模板 |
| `系统架构` | 设计系统架构和数据建模 | `架构`, `architecture` | 设计文档 |

## 技术栈

```
┌─────────────────────────────────────────────────────────────┐
│                      技术栈总览                              │
├─────────────────┬─────────────────┬─────────────────────────┤
│     层级        │     技术        │         用途            │
├─────────────────┼─────────────────┼─────────────────────────┤
│   运行时        │   Python 3.8+   │   脚本执行、数据处理    │
├─────────────────┼─────────────────┼─────────────────────────┤
│   前端框架      │   React/Vue     │   UI 组件开发           │
├─────────────────┼─────────────────┼─────────────────────────┤
│   文档处理      │   python-docx   │   Word 文档操作         │
│                 │   PyPDF2        │   PDF 文档处理          │
│                 │   openpyxl      │   Excel 表格处理        │
├─────────────────┼─────────────────┼─────────────────────────┤
│   版本控制      │   Git           │   代码版本管理          │
├─────────────────┼─────────────────┼─────────────────────────┤
│   协议          │   MCP           │   Model Context Protocol│
├─────────────────┼─────────────────┼─────────────────────────┤
│   IDE 集成      │   Trae IDE      │   开发环境集成          │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## 项目结构

```
Expert-Suite-Skills/
├── 01-编程相关/                    # 编程领域技能
│   ├── 代码审查/
│   │   ├── SKILL.md               # 技能定义
│   │   └── references/            # 参考资料
│   ├── 代码生成/
│   ├── Bug诊断/
│   ├── 重构建议/
│   ├── 技术选型/
│   ├── API设计/
│   ├── 测试用例生成/
│   ├── 文档生成/
│   ├── 前端设计/
│   ├── 测试驱动开发/
│   ├── Git工作树/
│   └── MCP服务器构建/
│
├── 02-写作与语言/                  # 写作领域技能
│   ├── 算法艺术/
│   ├── 品牌指南/
│   ├── Canvas设计/
│   ├── 前端设计(高级)/
│   ├── 主题工厂/
│   └── 网络小说创作/
│
├── 03-文档与幻灯片/                # 文档处理技能
│   ├── 文档协作/
│   ├── DOCX处理/
│   ├── PDF处理/
│   ├── PPTX处理/
│   └── XLSX处理/
│
├── 04-安全与法律/                  # 合规技能
│   └── 合规检查/
│
├── 05-系统与集成/                  # 系统技能
│   ├── MCP构建器/
│   ├── 技能创建/
│   └── 系统架构/
│
├── 专家套件创建指导/               # 创建新套件指南
│   ├── SKILL.md
│   └── references/
│
└── README.md                       # 本文件
```

## 开发指南

### 创建新技能

1. **规划技能**
   - 确定技能的目标和范围
   - 设计触发词和使用场景
   - 准备参考资料和示例

2. **创建目录结构**
   ```bash
   mkdir -p "01-编程相关/新技能/references"
   ```

3. **编写 SKILL.md**
   ```markdown
   ---
   name: 技能名称
   description: 技能描述
   triggers: [触发词1, 触发词2]
   version: 1.0.0
   author: 作者名
   ---

   # 技能名称

   ## 概述
   简要描述技能的功能和用途

   ## 使用方法
   详细的使用说明

   ## 示例
   实际使用示例

   ## 参考资料
   相关资源链接
   ```

4. **测试技能**
   - 在 Trae IDE 中加载技能
   - 测试各种触发场景
   - 验证输出质量

### 代码规范

- 遵循 PEP 8 Python 编码规范
- 使用 Markdown 编写文档
- 保持目录结构清晰一致

## 路线图

```
2024 Q4                    2025 Q1                    2025 Q2
   │                          │                          │
   ▼                          ▼                          ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ • 核心技能  │         │ • AI 集成   │         │ • 企业版    │
│ • 基础文档  │   ───►  │ • 自动化    │   ───►  │ • 团队协作  │
│ • 初始测试  │         │ • 性能优化  │         │ • 定制服务  │
└─────────────┘         └─────────────┘         └─────────────┘
```

**近期计划：**
- [ ] 增加更多编程语言支持 (Rust, Go, TypeScript)
- [ ] 实现技能版本管理和自动更新
- [ ] 添加单元测试覆盖率 > 80%
- [ ] 支持自定义技能模板
- [ ] 集成 CI/CD 自动化测试

**长期目标：**
- [ ] 构建技能市场，支持社区贡献
- [ ] 实现跨 IDE 平台支持 (VS Code, Cursor)
- [ ] 提供企业级部署方案
- [ ] 建立技能质量认证体系

## 常见问题 (FAQ)

### Q1: 如何在 Trae IDE 中安装这些技能？

**A:** 将技能目录复制到 Trae IDE 的 Skills 目录即可：
- Windows: `%APPDATA%\Trae\Skills\`
- macOS: `~/Library/Application Support/Trae/Skills/`
- Linux: `~/.config/trae/skills/`

### Q2: 可以同时使用多个技能吗？

**A:** 可以。技能之间相互独立，您可以根据需要同时启用多个技能。

### Q3: 如何创建自定义技能？

**A:** 参考 `专家套件创建指导` 目录中的模板和指南，按照标准格式创建即可。

### Q4: 技能是否支持多语言？

**A:** 目前主要支持中文，部分技能支持英文。欢迎贡献多语言翻译。

### Q5: 遇到问题如何反馈？

**A:** 请在 GitHub Issues 中提交问题，包含以下信息：
- 使用的技能名称
- 输入内容
- 期望输出 vs 实际输出
- 错误日志（如有）

## Contributing

我们欢迎社区贡献！请遵循以下流程：

1. **Fork 本仓库**
2. **创建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建 Pull Request**

### 贡献指南

- 确保代码符合项目规范
- 添加必要的测试用例
- 更新相关文档
- 提交前运行测试确保通过

详见 [CONTRIBUTING.md](CONTRIBUTING.md)（如有）

## License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

```
MIT License

Copyright (c) 2024 weksbwrx62862

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Security

### 安全承诺

- 所有技能代码经过安全审查
- 不收集或上传用户数据
- 定期更新依赖以修复安全漏洞

### 报告安全问题

如发现安全漏洞，请通过以下方式报告：
- **邮箱**: [security@example.com]（如有）
- **GitHub**: 创建标记为 "security" 的 Issue

我们承诺在 48 小时内响应安全问题。

## 致谢

感谢以下开源项目和社区：

- [Trae IDE](https://www.trae.ai/) - 提供开发环境支持
- [Python](https://www.python.org/) - 核心运行时
- [p5.js](https://p5js.org/) - 算法艺术支持
- 所有贡献者和用户

特别感谢 **qoder 社区** 为 AI 专家套件标准化所做的开创性工作。

---

<div align="center">

**让 AI 成为你的超级助手**

[⬆ 回到顶部](#-专家-skill-集合)

---

Made with ❤️ by [weksbwrx62862](https://github.com/weksbwrx62862)

</div>