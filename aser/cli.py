import cmd
import sys
import os
import time
from rich.console import Console
from rich.spinner import Spinner
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
from rich.style import Style
from aser.agent import Agent

import time

class Cli(cmd.Cmd):

    def __init__(self, agent):
        super().__init__()
        self.console = Console()

        self.uid = time.time()

        self.agent = agent

        intro_text = Text()

        intro_text.append(
            "How can I assist you today? (Type 'help' for commands)", style="green"
        )

        self.intro = intro_text
        self.prompt = f"{self.agent.name} > "

    def do_chat(self, arg):
        print(arg)
        with self.console.status("Cooking up your answer...", spinner="dots") as status:
            result = self.agent.chat(arg)
            # result_text = Text()
            # result_text.append(result, style="green")
            default_style = Style(color="green")
            md = Markdown(
                result,
                code_theme="monokai",
                hyperlinks=True,
                style=default_style,
            )

            self.console.print(md)

    def do_help(self, arg):

        help_text = Text()
        help_text.append("\n", style="cyan")
        help_text.append("  enter text directly to start chatting \n", style="cyan")
        help_text.append("  help  - show this help information\n", style="cyan")
        help_text.append("  clear - clear chat history\n", style="cyan")
        help_text.append("  exit  - exit program\n", style="cyan")
        self.console.print(
            Panel(help_text, title="Help", expand=False, border_style="cyan")
        )

    def do_clear(self, arg):
        os.system("cls" if os.name == "nt" else "clear")

    def do_exit(self, arg):

        return True

    def default(self, arg):
        self.do_chat(arg)

    def cmdloop(self, intro=None):
        self.console.print(self.intro)
        try:
            super(Cli, self).cmdloop(intro="")
        except KeyboardInterrupt:
            print("\nBye!")
            return




