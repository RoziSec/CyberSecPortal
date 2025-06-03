#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import subprocess
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.text import Text

from config import SUPPORTED_EXTENSIONS
from utils.terminal import KaliTerminal

console = Console()
terminal = KaliTerminal()


def launch_tool(tool):
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 设置工作目录为项目根目录
    os.chdir(project_root)

    # 获取工具的相对路径
    path = tool["path"]
    # 将相对路径转换为绝对路径
    abs_path = os.path.abspath(path)

    tool_type = tool["type"]
    tool_name = tool["name"]

    if tool_type == "exe":
        # 假设在工具配置中添加一个 "launch_method" 字段来指定启动方式
        launch_method = tool.get("launch_method", "direct")
        if launch_method == "direct":
            launch_config = SUPPORTED_EXTENSIONS["exe"][0]
        else:
            launch_config = SUPPORTED_EXTENSIONS["exe"][1]
    else:
        launch_config = SUPPORTED_EXTENSIONS.get(tool_type, {})

    type_icon = launch_config.get("icon", "📄")

    if not launch_config:
        console.print(f"[bold red]❌ 不支持的文件类型: {tool_type}[/bold red]")
        return False

    # 显示启动前的命令行模拟
    terminal.print_banner(f"🚀 启动 {tool_name}", f"正在准备运行 {type_icon} {tool_type} 程序", "green")

    # 显示模拟的启动命令序列
    terminal.simulate_command("chmod +x " + abs_path, f"[ ✓ ] 设置执行权限")

    # 处理参数
    parameters = tool.get("parameters", "")
    if "{url}" in parameters:
        url = terminal.ask("请输入目标URL: ")
        parameters = parameters.replace("{url}", url)

    # 设置当前工作目录为VBS脚本所在的目录
    vbs_dir = os.path.dirname(abs_path)
    os.chdir(vbs_dir)

    if launch_config["method"] == "direct":
        cmd = f"{abs_path} {parameters}"
        terminal.simulate_command(cmd, "正在启动...")
    else:
        cmd = f"{launch_config['command']} {abs_path} {parameters}"
        terminal.simulate_command(cmd, "正在启动...")

    # 检查文件是否存在
    if not os.path.exists(abs_path):
        # 对于演示目的，可以模拟工具路径不存在的情况
        console.print(Panel(
            Text.assemble(
                Text("⚠️ 注意: ", style="bold yellow"),
                Text(f"工具路径不存在: {abs_path}\n", style="yellow"),
                Text("这是一个演示环境，将模拟启动 ", style="yellow"),
                Text(tool_name, style="bold yellow")
            ),
            border_style="yellow"
        ))

        # 显示启动进度条
        with Progress(
                SpinnerColumn("dots"),
                TextColumn(f"[bold green]🚀 正在启动 {tool_name}...[/bold green]"),
                BarColumn(complete_style="green", finished_style="green"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
        ) as progress:
            task = progress.add_task(f"启动 {tool_name}", total=100)

            # 模拟启动过程
            for _ in range(100):
                time.sleep(0.03)
                progress.update(task, advance=1)

        # 模拟工具执行
        console.print(f"[bold green]✅ {tool_name} 已启动[/bold green]")

        # 为了演示效果，显示一些随机的"执行输出"
        outputs = [
            f"{tool_name} v{tool.get('version', '1.0')} 正在运行中...",
            f"正在扫描目标...",
            f"发现 {random.randint(3, 15)} 个开放端口",
            f"分析结果中...",
            f"生成报告: report_{int(time.time())}.txt"
        ]

        for output in outputs:
            time.sleep(random.uniform(0.8, 1.5))
            console.print(f"[dim]{output}[/dim]")

        time.sleep(0.5)
        console.print(f"[bold green]✅ {tool_name} 执行完成[/bold green]")
        return True

    # 实际启动工具
    try:
        # 显示启动进度条
        with Progress(
                SpinnerColumn("dots"),
                TextColumn(f"[bold green]🚀 正在启动 {tool_name}...[/bold green]"),
                BarColumn(complete_style="green", finished_style="green"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
        ) as progress:
            task = progress.add_task(f"启动 {tool_name}", total=100)

            # 模拟启动过程
            for _ in range(100):
                time.sleep(0.02)
                progress.update(task, advance=1)

        console.print(f"[bold green]✅ {tool_name} 已启动，正在执行...[/bold green]")

        if launch_config["method"] == "direct":
            # 直接执行文件（如exe）
            subprocess.run([abs_path, *parameters.split()], check=True)
        else:
            # 通过命令执行文件（如py, bat, jar, vbs）
            cmd_parts = launch_config["command"].split()
            if cmd_parts:
                subprocess.run([*cmd_parts, abs_path, *parameters.split()], check=True)
            else:
                subprocess.run([abs_path, *parameters.split()], check=True, shell=True)

        console.print(f"[bold green]✅ {tool_name} 执行完成[/bold green]")
        return True

    except subprocess.SubprocessError as e:
        console.print(Panel(
            Text.assemble(
                Text("❌ 错误: ", style="bold red"),
                Text(f"启动工具时出错\n\n", style="red"),
                Text(str(e), style="yellow")
            ),
            title=f"启动 {tool_name} 失败",
            border_style="red"
        ))
        return False
