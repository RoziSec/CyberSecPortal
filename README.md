# 🛡️ 终端安全工具集 🛡️

一个模拟Kali Linux风格的安全工具启动器，提供分类管理和便捷启动功能。

## ✨ 功能特点

- 🔐 **安全认证**: 启动时需进行密码验证，三次错误后自动锁定系统
- 📊 **分类管理**: 按功能对安全工具进行分类展示
- 🚀 **多格式支持**: 支持启动多种文件格式，包括exe、bat、vbs、jar、py等
- 💻 **终端风格**: 模拟Kali Linux终端风格的交互界面
- 🎨 **美观界面**: 使用Rich库提供丰富的文本格式和颜色
- 🔄 **易于扩展**: 模块化设计，易于添加新工具和功能

## 📋 系统要求

- Python 3.7+
- Rich 库 (`pip install rich`)

## 🚀 快速开始

1. 克隆本仓库或下载源码
2. 确保安装了所有依赖: `pip install -r requirements.txt`
3. 运行启动脚本: `python run.py`

## 📁 项目结构
```
CyberSecPortal/

├── run.py # 启动脚本

├── main.py # 主程序入口

├── config.py # 配置文件

├── utils/

│ ├── init.py

│ ├── auth.py # 认证相关功能

│ ├── launcher.py # 启动器核心功能

│ ├── ui.py # 界面相关功能

│ └── terminal.py # 终端模拟功能

└── data/

└── tools.json # 工具配置数据
```

## ⚙️ 配置说明

系统默认管理员密码为 `admin123`，可在 `config.py` 文件中修改。

## 🔧 扩展方法

### 添加新工具

编辑 `data/tools.json` 文件，按照现有格式添加新的工具项目。

### 添加新分类

在 `data/tools.json` 中创建新的分类键，并在 `config.py` 的 `CATEGORY_DESCRIPTIONS` 中添加对应的描述信息。

### 支持新文件类型

在 `config.py` 的 `SUPPORTED_EXTENSIONS` 字典中添加新的文件类型及启动方式。

## 📜 许可证

此项目基于 MIT 许可证发布。

## 👤 作者

开发者：[Norah C.IV]
