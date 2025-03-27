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
from aser.memory import Memory
import time
from aser.tools import Tools
from aser.toolkits import deepgram


class Cli(cmd.Cmd):

    def __init__(self):
        super().__init__()
        self.console = Console()

        self.uid = time.time()
        self.memory = Memory(type="sqlite")

        tools = Tools()
        tools.load_toolkits([deepgram])
        self.agent = Agent(
            name="aser agent", model="gpt-3.5-turbo", memory=self.memory, tools=tools
        )
        intro_text = Text()

        intro_text.append(
            "How can I assist you today? (Type 'help' for commands)", style="green"
        )

        self.intro = intro_text
        self.prompt = "aser> "

    def do_chat(self, arg):
        with self.console.status("thinking", spinner="dots") as status:
            result = self.agent.chat(arg, uid=self.uid)
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
        self.memory.clear(self.uid)
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


if __name__ == "__main__":
    Cli().cmdloop()
