#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import platform

from rich.box import ROUNDED, DOUBLE
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from config import CATEGORY_DESCRIPTIONS
from utils.terminal import KaliTerminal

console = Console()
terminal = KaliTerminal()


def clear_screen():
    """清屏函数，兼容不同操作系统"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def load_tools():
    """加载工具配置数据"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'data', 'tools.json')
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果文件不存在或格式错误，返回默认数据
        return {
            "信息收集": [
                {"name": "Nmap", "description": "网络扫描工具", "path": "tools/nmap.exe", "type": "exe"},
                {"name": "Whois查询", "description": "域名信息查询", "path": "tools/whois.py", "type": "py"},
            ],
            "漏洞扫描": [
                {"name": "OpenVAS", "description": "开源漏洞扫描器", "path": "tools/openvas.bat", "type": "bat"},
                {"name": "SQLMap", "description": "SQL注入检测工具", "path": "tools/sqlmap.py", "type": "py"},
            ],
            "漏洞利用": [
                {"name": "Metasploit", "description": "渗透测试框架", "path": "tools/msf.bat", "type": "bat"},
                {"name": "ExploitPack", "description": "漏洞利用集合", "path": "tools/exploit.jar", "type": "jar"},
            ],
            "抓包工具": [
                {"name": "Wireshark", "description": "网络协议分析工具", "path": "tools/wireshark.exe", "type": "exe"},
                {"name": "Burp Suite", "description": "Web应用安全测试", "path": "tools/burp.vbs", "type": "vbs"},
            ],
        }


def display_categories():
    """显示工具分类并返回用户选择"""
    tools_data = load_tools()  # 确保每次都重新加载工具数据
    categories = list(tools_data.keys())

    terminal.print_banner("安全工具分类", "Security Tool Categories", "blue")

    # 不使用emoji创建表格，完全去除图标列
    table = Table(
        box=ROUNDED,
        title_style="bold cyan",
        border_style="blue",
        padding=(0, 1)
    )

    table.add_column("序号", style="cyan", justify="center", width=5)
    # 移除图标列
    table.add_column("分类名称", style="green")
    table.add_column("描述", style="yellow")

    for i, category in enumerate(categories, 1):
        category_info = CATEGORY_DESCRIPTIONS.get(category, {"desc": "无描述信息", "icon": "📁", "color": "white"})
        description = category_info["desc"]
        # 去除emoji图标，只使用文本
        table.add_row(str(i), category, description)

    # 添加退出选项，不使用emoji
    table.add_row(str(len(categories) + 1), "退出程序", "退出系统并返回命令行")

    # 显示表格
    console.print(table)
    console.print()

    while True:
        result = terminal.ask("请选择工具分类", default="")  # 将默认值设为空

        if result == "exit":
            return "exit"

        if result == "":  # 如果输入为空，继续等待输入
            continue

        try:
            choice = int(result)
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                terminal.simulate_command(f"cd categories/{category}", f"已进入 {category} 分类")
                return category
            elif choice == len(categories) + 1:
                terminal.simulate_command("exit", "正在退出程序...")
                return "exit"
            else:
                console.print("[bold red]无效的选择，请重试[/bold red]")
        except ValueError:
            console.print("[bold red]请输入有效的数字[/bold red]")


def display_tools(category):
    """显示指定分类下的工具并返回用户选择"""
    tools_data = load_tools()  # 确保每次都重新加载工具数据
    tools = tools_data.get(category, [])

    category_info = CATEGORY_DESCRIPTIONS.get(category, {"desc": "无描述信息", "icon": "📁", "color": "blue"})

    # 不使用emoji在标题中
    terminal.print_banner(
        f"{category} 工具列表",
        f"{category_info['desc']}",
        category_info["color"]
    )

    # 创建无emoji的表格
    table = Table(
        box=ROUNDED,
        border_style=category_info["color"],
        padding=(0, 1)
    )

    table.add_column("序号", style="cyan", justify="center", width=5)
    # 将类型列改为文本而非图标
    table.add_column("类型", style="bright_black", width=6)
    table.add_column("工具名称", style="green")
    table.add_column("描述", style="yellow")
    table.add_column("版本", style="blue", width=8, justify="center")

    for i, tool in enumerate(tools, 1):
        version = tool.get("version", "未知")
        tool_type = tool["type"]
        # 使用文本替换emoji图标
        table.add_row(str(i), tool_type.upper(), tool["name"], tool["description"], version)

    # 添加返回选项，不使用emoji
    table.add_row(str(len(tools) + 1), "", "返回上级菜单", "返回工具分类选择", "")

    # 显示表格
    console.print(table)
    console.print()

    while True:
        result = terminal.ask("请选择工具", default="")  # 将默认值设为空

        if result == "exit":
            return "exit"
        elif result.lower() == 'b':
            terminal.simulate_command("cd ..", "返回上级目录")
            return "back"

        if result == "":  # 如果输入为空，继续等待输入
            continue

        try:
            choice = int(result)
            if 1 <= choice <= len(tools):
                selected_tool = tools[choice - 1]
                terminal.simulate_command(f"info {selected_tool['name']}", f"查看 {selected_tool['name']} 详细信息")

                # 展示工具的详细信息
                tool_result = display_tool_details(selected_tool)
                if tool_result == "back":
                    # 如果用户在详情页选择返回，重新显示工具列表
                    clear_screen()
                    terminal.print_banner(
                        f"{category} 工具列表",
                        f"{category_info['desc']}",
                        category_info["color"]
                    )
                    console.print(table)
                    console.print()
                    continue
                elif tool_result == "exit":
                    return "exit"

                return selected_tool
            elif choice == len(tools) + 1:
                terminal.simulate_command("cd ..", "返回上级目录")
                return "back"
            else:
                console.print("[bold red]无效的选择，请重试[/bold red]")
        except ValueError:
            if result.lower() == 'b':
                terminal.simulate_command("cd ..", "返回上级目录")
                return "back"
            else:
                console.print("[bold red]请输入有效的数字或命令[/bold red]")

def display_tool_details(tool):
    """显示工具的详细信息"""
    clear_screen()

    # 收集工具详细信息，如果没有则显示默认值
    name = tool["name"]
    description = tool["description"]
    tool_type = tool["type"]
    version = tool.get("version", "未知")
    author = tool.get("author", "未知")
    website = tool.get("website", "无")
    usage = tool.get("usage", "无详细使用说明")

    # 显示工具信息标题，不使用emoji
    terminal.print_banner(f"{name} v{version}", "工具详细信息", "cyan")

    # 创建详细信息表格，不使用emoji
    info_table = Table(
        box=DOUBLE,
        show_header=False,
        border_style="bright_blue",
        padding=(0, 1)
    )

    info_table.add_column("属性", style="bold cyan", width=12)
    info_table.add_column("内容", style="yellow")

    info_table.add_row("工具名称", name)
    info_table.add_row("版本", version)
    info_table.add_row("类型", tool_type.upper())
    info_table.add_row("描述", description)
    info_table.add_row("开发者", author)
    info_table.add_row("官方网站", website)

    console.print(info_table)

    # 显示使用说明
    usage_panel = Panel(
        Markdown(f"## 使用说明\n\n{usage}"),
        title="使用指南",
        border_style="green",
        box=ROUNDED
    )
    console.print(usage_panel)

    # 显示启动提示，不使用emoji
    console.print()
    console.print("[bold green]准备启动此工具...[/bold green]")
    console.print("[bold yellow]提示: 启动后工具将在单独的窗口中运行[/bold yellow]")
    console.print()

    # 选项提示，不使用emoji
    options_text = (
        "[dim]输入选项:[/dim]\n"
        "[green]Enter[/green] - 启动工具\n"
        "[yellow]b[/yellow] - 返回工具列表\n"
        "[red]x[/red] - 退出程序"
    )
    console.print(Panel(options_text, title="操作选项", border_style="blue", width=30))

    # 等待用户确认
    result = terminal.ask("请选择操作", default="")

    if result.lower() == 'b':
        return "back"
    elif result.lower() == 'x' or result == "exit":
        return "exit"

    return True
