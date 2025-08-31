from aser.agent import Agent
from aser.cli import Cli
agent = Agent(name="aser agent", model="gpt-3.5-turbo")
cli = Cli(agent)
cli.cmdloop()