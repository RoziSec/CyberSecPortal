#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn, TimeElapsedColumn

from config import CONFIG
from utils.terminal import KaliTerminal

console = Console()
terminal = KaliTerminal()


def authenticate():
    """用户身份验证函数"""
    clear_screen()

    # 创建ASCII艺术标题
    title_art = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║    _____     __           ____        ___           __       __  ║
    ║   / ___/_ __/ /  ___ ____/ __/__ ____/ _ \___  ____/ /____ _/ /  ║
    ║  / /__/ // / _ \/ -_) __/\ \/ -_) __/ ___/ _ \/ __/ __/ _ `/ /   ║
    ║  \___/\_, /_.__/\__/_/ /___/\__/\__/_/   \___/_/  \__/\_,_/_/    ║
    ║       /___/                                                      ║
    ╚══════════════════════════════════════════════════════════════════╝
    """

    version_info = f"🛡️  终端安全工具集 v{CONFIG['app_version']}  🛡️"

    console.print(title_art, style="bold blue", highlight=False)
    console.print(version_info, style="bold cyan", justify="center")

    terminal.print_banner("🔐 安全工具集终端 🔐", "Security Tools Terminal", "blue")

    # 模拟启动终端序列
    terminal.simulate_command("sudo service postgresql start", "[ ✓ ] 数据库服务已启动")
    terminal.simulate_command("sudo service openssh start", "[ ✓ ] SSH服务已启动")
    terminal.simulate_command("echo '准备启动安全工具集...'", "准备启动安全工具集...")
    terminal.simulate_command("./security_toolkit.py", "正在初始化安全工具集...")

    console.print()
    console.print("[bold blue]🛡️  终端程序启动器 🛡️[/bold blue]", justify="center")
    console.print("[bold yellow]⚠️  请进行身份验证 ⚠️[/bold yellow]", justify="center")
    console.print()

    attempts = 0
    while attempts < CONFIG["max_attempts"]:
        password = terminal.password_prompt("输入系统访问密码: ")

        if password == CONFIG["password"]:
            console.print("[bold green]✅ 验证成功！欢迎使用[/bold green]")

            # 添加加载进度条
            console.print()
            with Progress(
                    SpinnerColumn("dots"),
                    TextColumn("[bold blue]🔄 正在加载系统资源...[/bold blue]"),
                    BarColumn(complete_style="green", finished_style="green"),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeElapsedColumn(),
                    console=console
            ) as progress:
                task = progress.add_task("[green]加载中...", total=100)

                # 模拟加载过程
                while not progress.finished:
                    progress.update(task, advance=0.9)
                    time.sleep(0.05)

            console.print("[bold green]🚀 系统准备就绪![/bold green]")
            return True
        else:
            attempts += 1
            remaining = CONFIG["max_attempts"] - attempts
            if remaining > 0:
                console.print(f"[bold red]❌ 密码错误！还有{remaining}次尝试机会[/bold red]")
            else:
                console.print("[bold red]⛔ 密码错误次数过多，系统锁定！[/bold red]")
                terminal.simulate_command("sudo service apparmor start", "正在锁定系统...")
                time.sleep(1)  # 延迟一秒，增强安全感

    return False


def clear_screen():
    """清屏函数"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
