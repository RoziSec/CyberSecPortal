#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 系统配置
CONFIG = {
    "password": "admin123",  # 系统密码，实际应用中应加密存储
    "max_attempts": 3,  # 最大密码尝试次数
    "app_version": "2.1.0",  # 应用版本号
    "terminal_style": "kali",  # 终端样式 (kali, ubuntu, windows)
}

# 支持的文件类型和启动方式
SUPPORTED_EXTENSIONS = {
    "vbs": {"method": "cmd", "command": "cscript", "icon": "🌐"},
    "exe": [
        {"method": "direct", "command": "", "icon": "⚙️"},
        {"method": "cmd", "command": "", "icon": "⚙️"}
    ],
    "bat": {"method": "cmd", "command": "", "icon": "🔧"},
    "jar": {"method": "cmd", "command": "java -jar", "icon": "☕"},
    "py": {"method": "cmd", "command": "python", "icon": "🐍"},
    "sh": {"method": "cmd", "command": "bash", "icon": "🐚"},
    "php": {"method": "cmd", "command": "php", "icon": "🌐"},
    "js": {"method": "cmd", "command": "node", "icon": "📱"},
}

# 工具分类描述和图标
CATEGORY_DESCRIPTIONS = {
    "信息收集": {
        "desc": "用于收集目标系统、网络和域名等信息的工具集",
        "icon": "🔍",
        "color": "cyan"
    },
    "漏洞扫描": {
        "desc": "用于发现系统、网络和应用程序中潜在漏洞的工具集",
        "icon": "🔬",
        "color": "green"
    },
    "漏洞利用": {
        "desc": "利用已知漏洞获取目标系统访问权限的工具集",
        "icon": "🎯",
        "color": "red"
    },
    "抓包工具": {
        "desc": "用于捕获、分析和修改网络流量的工具集",
        "icon": "📦",
        "color": "blue"
    },
    "密码工具": {
        "desc": "用于密码破解、生成和管理的工具集",
        "icon": "🔑",
        "color": "magenta"
    },
    "社会工程": {
        "desc": "用于社会工程学攻击和防御的工具集",
        "icon": "👤",
        "color": "yellow"
    },
    "取证分析": {
        "desc": "用于数字取证和数据恢复的工具集",
        "icon": "🔎",
        "color": "bright_blue"
    },
    "加密工具": {
        "desc": "用于加密、解密和编码转换的工具集",
        "icon": "🔒",
        "color": "bright_green"
    },
    "网络工具": {
        "desc": "用于网络连接、扫描和配置的工具集",
        "icon": "🌐",
        "color": "bright_cyan"
    },
}

# 系统消息
SYSTEM_MESSAGES = {
    "welcome": "欢迎使用安全工具集终端",
    "goodbye": "感谢使用安全工具集终端，再见!",
    "loading": "正在加载系统资源...",
    "ready": "系统准备就绪!",
    "auth_required": "请进行身份验证",
    "auth_success": "验证成功！欢迎使用",
    "auth_fail": "验证失败，程序退出!",
    "invalid_choice": "无效的选择，请重试",
}
