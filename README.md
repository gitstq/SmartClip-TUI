<div align="center">

# 🚀 SmartClip-TUI

**AI驱动的终端剪贴板管理器 | AI-Powered Terminal Clipboard Manager**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-orange)]()
[![TUI](https://img.shields.io/badge/TUI-Textual-purple)](https://textual.textualize.io)

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**SmartClip-TUI** 是一款专为开发者打造的智能终端剪贴板管理器。它解决了日常开发中频繁复制粘贴导致的历史记录丢失、内容难以检索、代码片段管理混乱等痛点。

**灵感来源**：观察到现在开发者每天需要在终端、浏览器、IDE之间频繁切换复制内容，但系统自带的剪贴板只能保存最近一条记录，导致大量有价值的信息（如API密钥、代码片段、命令行）丢失。

**自研差异化亮点**：
- 🤖 **AI智能分类**：自动识别URL、代码、命令、JSON、密码等类型
- 🎯 **代码语言检测**：自动识别Python、JavaScript、Go、Rust等20+语言
- 🔒 **隐私保护**：自动识别并标记敏感内容（密码、API密钥）
- 📊 **使用统计**：追踪使用频率，智能排序

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 🎨 **精美TUI界面** | 基于Textual构建，支持鼠标和键盘操作 | ✅ |
| 🔍 **模糊搜索** | 支持内容、标签、类型多维度搜索 | ✅ |
| 🏷️ **智能标签** | 自动提取标签，支持自定义标签管理 | ✅ |
| ⭐ **收藏系统** | 快速收藏常用内容，一键访问 | ✅ |
| 💾 **SQLite持久化** | 本地存储，数据安全，支持海量记录 | ✅ |
| 🌐 **跨平台** | 支持Windows、macOS、Linux | ✅ |
| ⌨️ **快捷键** | 全键盘操作，提升效率 | ✅ |
| 📈 **统计分析** | 类型分布、使用频率统计 | ✅ |

### 🚀 快速开始

#### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10+/macOS 10.15+/Linux

#### 安装步骤

```bash
# 使用pip安装
pip install smartclip-tui

# 或使用源码安装
git clone https://github.com/gitstq/SmartClip-TUI.git
cd SmartClip-TUI
pip install -e .
```

#### 启动应用

```bash
# 启动TUI界面
smartclip tui

# 或使用短命令
sclip tui
```

### 📖 详细使用指南

#### TUI界面操作

| 快捷键 | 功能 |
|--------|------|
| `↑/↓` | 浏览剪贴板历史 |
| `Enter` | 查看详情/编辑 |
| `c` | 复制选中项到剪贴板 |
| `f` | 切换收藏状态 |
| `d` | 删除选中项 |
| `s` | 聚焦搜索框 |
| `r` | 刷新列表 |
| `q` | 退出应用 |

#### CLI命令

```bash
# 添加当前剪贴板内容
smartclip add

# 添加指定内容
smartclip add "https://github.com/user/repo" --type url --tag git --tag repo

# 列出历史记录
smartclip list --limit 50

# 搜索内容
smartclip search "python"

# 复制指定ID的内容
smartclip copy 123

# 查看统计
smartclip stats

# 删除指定ID的内容
smartclip delete 123

# 切换收藏
smartclip favorite 123
```

### 💡 设计思路与迭代规划

#### 技术选型原因

- **Textual**: 选择Textual而非其他TUI库，因为它提供了现代化的组件系统和CSS样式支持，开发效率高
- **SQLite**: 轻量级本地数据库，无需额外服务，适合个人工具场景
- **pyperclip**: 跨平台剪贴板操作库，兼容性好

#### 后续迭代计划

- [ ] 🌐 **Web同步**: 支持多设备剪贴板同步
- [ ] 🤖 **AI摘要**: 集成LLM为长文本生成智能摘要
- [ ] 🔍 **正则搜索**: 支持正则表达式高级搜索
- [ ] 📤 **导出功能**: 支持导出为JSON/Markdown
- [ ] 🔌 **插件系统**: 支持自定义插件扩展

### 📦 打包与部署

```bash
# 开发环境设置
make setup

# 运行测试
make test

# 代码格式化
make format

# 构建包
make build

# 安装到本地
pip install dist/smartclip_tui-1.0.0-py3-none-any.whl
```

### 🤝 贡献指南

欢迎提交Issue和PR！请遵循以下规范：

1. **Issue规范**: 描述问题、复现步骤、期望结果
2. **PR规范**: 使用Angular提交规范（feat/fix/docs/refactor）
3. **代码风格**: 使用Black格式化，flake8检查

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

**SmartClip-TUI** 是一款專為開發者打造的智慧終端機剪貼簿管理器。它解決了日常開發中頻繁複製貼上導致的歷史記錄遺失、內容難以檢索、程式碼片段管理混亂等痛點。

**靈感來源**：觀察到現在開發者每天需要在終端機、瀏覽器、IDE之間頻繁切換複製內容，但系統自帶的剪貼簿只能儲存最近一條記錄，導致大量有價值的資訊（如API金鑰、程式碼片段、命令列）遺失。

**自研差異化亮點**：
- 🤖 **AI智慧分類**：自動識別URL、程式碼、命令、JSON、密碼等類型
- 🎯 **程式語言檢測**：自動識別Python、JavaScript、Go、Rust等20+語言
- 🔒 **隱私保護**：自動識別並標記敏感內容（密碼、API金鑰）
- 📊 **使用統計**：追蹤使用頻率，智慧排序

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 🎨 **精美TUI介面** | 基於Textual構建，支援滑鼠和鍵盤操作 | ✅ |
| 🔍 **模糊搜尋** | 支援內容、標籤、類型多維度搜尋 | ✅ |
| 🏷️ **智慧標籤** | 自動提取標籤，支援自訂標籤管理 | ✅ |
| ⭐ **收藏系統** | 快速收藏常用內容，一鍵存取 | ✅ |
| 💾 **SQLite持久化** | 本地儲存，資料安全，支援海量記錄 | ✅ |
| 🌐 **跨平台** | 支援Windows、macOS、Linux | ✅ |
| ⌨️ **快速鍵** | 全鍵盤操作，提升效率 | ✅ |
| 📈 **統計分析** | 類型分佈、使用頻率統計 | ✅ |

### 🚀 快速開始

#### 環境要求

- **Python**: 3.8 或更高版本
- **作業系統**: Windows 10+/macOS 10.15+/Linux

#### 安裝步驟

```bash
# 使用pip安裝
pip install smartclip-tui

# 或使用原始碼安裝
git clone https://github.com/gitstq/SmartClip-TUI.git
cd SmartClip-TUI
pip install -e .
```

#### 啟動應用

```bash
# 啟動TUI介面
smartclip tui

# 或使用短命令
sclip tui
```

### 📖 詳細使用指南

#### TUI介面操作

| 快速鍵 | 功能 |
|--------|------|
| `↑/↓` | 瀏覽剪貼簿歷史 |
| `Enter` | 檢視詳情/編輯 |
| `c` | 複製選中項到剪貼簿 |
| `f` | 切換收藏狀態 |
| `d` | 刪除選中項 |
| `s` | 聚焦搜尋框 |
| `r` | 重新整理列表 |
| `q` | 退出應用 |

#### CLI命令

```bash
# 新增目前剪貼簿內容
smartclip add

# 新增指定內容
smartclip add "https://github.com/user/repo" --type url --tag git --tag repo

# 列出歷史記錄
smartclip list --limit 50

# 搜尋內容
smartclip search "python"

# 複製指定ID的內容
smartclip copy 123

# 檢視統計
smartclip stats

# 刪除指定ID的內容
smartclip delete 123

# 切換收藏
smartclip favorite 123
```

### 💡 設計思路與迭代規劃

#### 技術選型原因

- **Textual**: 選擇Textual而非其他TUI庫，因為它提供了現代化的元件系統和CSS樣式支援，開發效率高
- **SQLite**: 輕量級本地資料庫，無需額外服務，適合個人工具場景
- **pyperclip**: 跨平台剪貼簿操作庫，相容性好

#### 後續迭代計劃

- [ ] 🌐 **Web同步**: 支援多裝置剪貼簿同步
- [ ] 🤖 **AI摘要**: 整合LLM為長文字生成智慧摘要
- [ ] 🔍 **正規表示式搜尋**: 支援正規表示式進階搜尋
- [ ] 📤 **匯出功能**: 支援匯出為JSON/Markdown
- [ ] 🔌 **外掛系統**: 支援自訂外掛擴充

### 📦 打包與部署

```bash
# 開發環境設定
make setup

# 執行測試
make test

# 程式碼格式化
make format

# 建置套件
make build

# 安裝到本地
pip install dist/smartclip_tui-1.0.0-py3-none-any.whl
```

### 🤝 貢獻指南

歡迎提交Issue和PR！請遵循以下規範：

1. **Issue規範**: 描述問題、復現步驟、期望結果
2. **PR規範**: 使用Angular提交規範（feat/fix/docs/refactor）
3. **程式碼風格**: 使用Black格式化，flake8檢查

### 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Introduction

**SmartClip-TUI** is an AI-powered terminal clipboard manager designed for developers. It solves the pain points of lost clipboard history, difficult content retrieval, and chaotic code snippet management during daily development.

**Inspiration**: Observing that developers frequently switch between terminal, browser, and IDE for copying content, but the system clipboard only stores the most recent item, causing valuable information (API keys, code snippets, commands) to be lost.

**Differentiation Highlights**:
- 🤖 **AI Smart Classification**: Auto-detect URLs, code, commands, JSON, passwords
- 🎯 **Code Language Detection**: Auto-identify Python, JavaScript, Go, Rust, and 20+ languages
- 🔒 **Privacy Protection**: Auto-detect and flag sensitive content (passwords, API keys)
- 📊 **Usage Statistics**: Track usage frequency with smart sorting

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🎨 **Beautiful TUI** | Built with Textual, supports mouse and keyboard | ✅ |
| 🔍 **Fuzzy Search** | Multi-dimensional search by content, tags, type | ✅ |
| 🏷️ **Smart Tags** | Auto-extract tags with custom tag management | ✅ |
| ⭐ **Favorites** | Quick bookmark frequently used content | ✅ |
| 💾 **SQLite Persistence** | Local storage, secure data, massive records support | ✅ |
| 🌐 **Cross-Platform** | Windows, macOS, Linux support | ✅ |
| ⌨️ **Shortcuts** | Full keyboard operation for efficiency | ✅ |
| 📈 **Analytics** | Type distribution and usage frequency stats | ✅ |

### 🚀 Quick Start

#### Requirements

- **Python**: 3.8 or higher
- **OS**: Windows 10+/macOS 10.15+/Linux

#### Installation

```bash
# Install via pip
pip install smartclip-tui

# Or install from source
git clone https://github.com/gitstq/SmartClip-TUI.git
cd SmartClip-TUI
pip install -e .
```

#### Launch

```bash
# Launch TUI
smartclip tui

# Or use short command
sclip tui
```

### 📖 Detailed Usage

#### TUI Shortcuts

| Shortcut | Action |
|----------|--------|
| `↑/↓` | Browse clipboard history |
| `Enter` | View details/edit |
| `c` | Copy selected to clipboard |
| `f` | Toggle favorite |
| `d` | Delete selected |
| `s` | Focus search box |
| `r` | Refresh list |
| `q` | Quit app |

#### CLI Commands

```bash
# Add current clipboard content
smartclip add

# Add specific content
smartclip add "https://github.com/user/repo" --type url --tag git --tag repo

# List history
smartclip list --limit 50

# Search content
smartclip search "python"

# Copy content by ID
smartclip copy 123

# View statistics
smartclip stats

# Delete content by ID
smartclip delete 123

# Toggle favorite
smartclip favorite 123
```

### 💡 Design & Roadmap

#### Tech Stack Rationale

- **Textual**: Chosen for its modern component system and CSS styling support
- **SQLite**: Lightweight local database, no extra services needed
- **pyperclip**: Cross-platform clipboard library with great compatibility

#### Roadmap

- [ ] 🌐 **Web Sync**: Multi-device clipboard synchronization
- [ ] 🤖 **AI Summary**: Integrate LLM for smart text summarization
- [ ] 🔍 **Regex Search**: Advanced regex search support
- [ ] 📤 **Export**: Export to JSON/Markdown formats
- [ ] 🔌 **Plugin System**: Custom plugin extension support

### 📦 Packaging & Deployment

```bash
# Setup dev environment
make setup

# Run tests
make test

# Format code
make format

# Build package
make build

# Install locally
pip install dist/smartclip_tui-1.0.0-py3-none-any.whl
```

### 🤝 Contributing

Issues and PRs are welcome! Please follow:

1. **Issue format**: Describe problem, reproduction steps, expected result
2. **PR format**: Use Angular commit convention (feat/fix/docs/refactor)
3. **Code style**: Use Black formatter, flake8 linter

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by SmartClip Team**

[⬆ Back to Top](#-smartclip-tui)

</div>
