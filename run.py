#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
安全工具集终端启动文件
此脚本用于检查环境依赖并启动主程序
"""

import subprocess
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

console = Console()


def check_dependencies():
    """检查所需的Python包是否已安装"""
    required_packages = ['rich']
    missing_packages = []

    console.print("[bold blue]🔍 检查依赖...[/bold blue]")

    with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]检查Python包...[/bold blue]"),
            console=console
    ) as progress:
        task = progress.add_task("检查中", total=len(required_packages))

        for package in required_packages:
            try:
                __import__(package)
                progress.update(task, advance=1)
                time.sleep(0.3)  # 添加延迟以便观察
            except ImportError:
                missing_packages.append(package)
                progress.update(task, advance=1)
                time.sleep(0.3)  # 添加延迟以便观察

    if missing_packages:
        console.print("[bold yellow]⚠️ 检测到缺少以下Python包:[/bold yellow]")
        for package in missing_packages:
            console.print(f"  - {package}")

        console.print("[bold blue]🔄 正在安装缺失的包...[/bold blue]")

        try:
            for package in missing_packages:
                console.print(f"安装 {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                console.print(f"[bold green]✅ {package} 安装成功[/bold green]")
        except subprocess.CalledProcessError:
            console.print(Panel(
                "❌ 安装依赖失败。请手动安装以下包:\n" +
                "\n".join([f"pip install {pkg}" for pkg in missing_packages]),
                title="错误",
                border_style="red"
            ))
            return False

    console.print("[bold green]✅ 所有依赖已满足[/bold green]")
    return True


def main():
    """主函数，启动工具集"""
    console.print(Panel(
        Text("终端安全工具集", style="bold blue"),
        subtitle="初始化中...",
        border_style="blue"
    ))

    if check_dependencies():
        console.print("[bold green]🚀 启动主程序...[/bold green]")
        time.sleep(1)
        try:
            from main import main as start_main
            start_main()
        except ImportError:
            console.print("[bold red]❌ 无法导入主程序。请确保main.py文件存在并且正确。[/bold red]")
    else:
        console.print("[bold red]❌ 依赖检查失败，无法启动程序。[/bold red]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⚠️ 用户中断，尝试安全退出...[/bold yellow]")
        try:
            from main import display_exit
            display_exit()
        except ImportError:
            console.print("[bold red]❌ 无法导入退出显示函数。直接退出程序。[/bold red]")
    except Exception as e:
        console.print(Panel(
            f"❌ 发生错误: {str(e)}",
            title="程序错误",
            border_style="red"
        ))