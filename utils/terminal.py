#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import os
import random
import time

from rich.console import Console
from rich.text import Text

console = Console()


class KaliTerminal:
    """模拟Kali Linux终端风格的交互界面"""

    def __init__(self):
        self.user = "kali"
        self.hostname = "sectools"
        # 随机生成一个IP地址作为终端显示
        self.ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
        self.current_dir = "~/toolkit"

    def prompt(self):
        """显示类似Kali的提示符"""
        user_host = Text(f"{self.user}@{self.hostname}", style="bold green")
        separator = Text(":", style="white")
        directory = Text(self.current_dir, style="bold blue")
        arrow = Text(" # ", style="bold red")

        prompt_text = Text.assemble(user_host, separator, directory, arrow)
        console.print(prompt_text, end="")

    def input(self, hidden=False):
        """获取用户输入，可选择是否隐藏输入内容"""
        if hidden:
            return getpass.getpass("")
        else:
            return input("")

    def execute_command(self, command):
        """模拟执行终端命令"""
        if command.lower() in ["clear", "cls"]:
            os.system("cls" if os.name == "nt" else "clear")
            return True

        if command.lower() in ["exit", "quit"]:
            return "exit"

        if command.lower() == "help":
            self._show_help()
            return True

        return False

    def _show_help(self):
        """显示帮助信息"""
        help_text = """
🔍 可用命令:
  • clear/cls - 清屏
  • exit/quit - 退出程序
  • help      - 显示此帮助信息
  • 数字      - 选择相应的选项
        """
        console.print(help_text, style="bold cyan")

    def ask(self, question, choices=None, default=None):
        """询问用户问题，可提供选项列表"""
        console.print(Text(f"❓ {question}", style="bold yellow"))

        if choices:
            for i, choice in enumerate(choices, 1):
                console.print(f"  {i}. {choice}")

        self.prompt()
        response = self.input()

        # 检查是否是命令
        cmd_result = self.execute_command(response)
        if cmd_result == "exit":
            return "exit"
        elif cmd_result:
            return self.ask(question, choices, default)

        # 如果用户没有输入，使用默认值
        if not response and default is not None:
            return default

        # 如果有选择列表，尝试解析数字输入
        if choices and response.isdigit():
            choice_num = int(response)
            if 1 <= choice_num <= len(choices):
                return choice_num

        return response

    def password_prompt(self, message="Password: "):
        """密码输入提示"""
        console.print(Text(f"🔒 {message}", style="bold yellow"), end="")
        return self.input(hidden=True)

    def print_banner(self, title, subtitle=None, style="green"):
        """打印终端风格的横幅"""
        width = console.width

        console.print("=" * width, style=f"bold {style}")

        # 居中显示标题
        padding = (width - len(title)) // 2
        if padding > 0:
            console.print(" " * padding + title, style=f"bold {style}")
        else:
            console.print(title, style=f"bold {style}")

        # 显示副标题
        if subtitle:
            padding = (width - len(subtitle)) // 2
            if padding > 0:
                console.print(" " * padding + subtitle, style=f"italic {style}")
            else:
                console.print(subtitle, style=f"italic {style}")

        console.print("=" * width, style=f"bold {style}")
        console.print()

    def simulate_typing(self, text, delay=0.03):
        """模拟打字效果"""
        for char in text:
            console.print(char, end="", highlight=False)
            time.sleep(delay)
        console.print()

    def simulate_command(self, command, output=None, error=False):
        """模拟运行命令及其输出"""
        self.prompt()
        self.simulate_typing(command)

        if output:
            if error:
                console.print(output, style="bold red")
            else:
                console.print(output)

        time.sleep(0.5)
