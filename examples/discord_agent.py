from esper.social.discord import DiscordClient
from esper.agent import Agent
agent=Agent(name="discord agent", description="discord agent",model="gpt-3.5-turbo")
discord_agent = DiscordClient(agent)
discord_agent.run()