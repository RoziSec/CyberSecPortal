#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from rich.box import HEAVY
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import CONFIG
from utils.auth import authenticate, clear_screen
from utils.launcher import launch_tool
from utils.terminal import KaliTerminal
from utils.ui import display_categories, display_tools


def display_welcome():
    """显示欢迎标题"""
    console = Console()
    clear_screen()

    # 添加系统信息表格
    table = Table(box=HEAVY, show_header=False, border_style="blue")
    table.add_column("属性", style="green")
    table.add_column("值", style="yellow")

    table.add_row("🔧 系统模式", CONFIG["terminal_style"].upper())
    table.add_row("📅 启动时间", time.strftime("%Y-%m-%d %H:%M:%S"))
    table.add_row("🔐 安全级别", "标准")
    table.add_row("📡 网络状态", "已连接")

    console.print(Panel(table, border_style="blue", title="系统信息", subtitle="准备就绪"))


def display_exit():
    """显示退出信息"""
    console = Console()
    terminal = KaliTerminal()

    clear_screen()

    # 显示退出信息
    goodbye_message = """
    🙏 感谢使用终端安全工具集 🙏

    🔒 系统已安全退出
    📊 会话摘要:
      • 启动时间: {start_time}
      • 结束时间: {end_time}
      • 总运行时间: {runtime}

    👋 再见!
    """.format(
        start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 300)),  # 假设运行了5分钟
        end_time=time.strftime("%Y-%m-%d %H:%M:%S"),
        runtime="00:05:00"  # 为简单起见使用固定值
    )

    console.print(Panel(goodbye_message, border_style="green", title="会话结束", subtitle="安全退出"))

    # 模拟关闭服务
    terminal.simulate_command("service postgresql stop", "[ ✓ ] 数据库服务已停止")
    terminal.simulate_command("service ssh stop", "[ ✓ ] SSH服务已停止")
    terminal.simulate_command("exit", "正在退出...")


def main():
    console = Console()
    terminal = KaliTerminal()

    display_welcome()

    # 验证用户身份
    if not authenticate():
        console.print("[bold red]❌ 验证失败，程序退出![/bold red]")
        sys.exit(1)

    while True:
        # 显示工具分类
        clear_screen()
        category = display_categories()

        # 如果用户选择退出
        if category == "exit":
            clear_screen()
            display_exit()
            break

        # 显示分类下的工具
        clear_screen()
        tool = display_tools(category)

        # 如果用户选择返回
        if tool == "back":
            continue
        elif tool == "exit":
            clear_screen()
            display_exit()
            break

        # 启动选中的工具
        if tool:
            launch_tool(tool)

            # 工具执行完后暂停
            console.print()
            result = terminal.ask("按Enter键返回主菜单，或输入'x'退出程序", default="")
            if result.lower() == 'x' or result == "exit":
                clear_screen()
                display_exit()
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # 捕获Ctrl+C
        console = Console()
        console.print("\n[bold yellow]⚠️ 检测到用户中断[/bold yellow]")
        console.print("[bold green]安全退出程序...[/bold green]")
        time.sleep(1)
        display_exit()
