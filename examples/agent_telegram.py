from amer.social.telegram import TelegramClient
from amer.agent import Agent
agent=Agent(name="telegram agent", description="telegram agent",model="gpt-3.5-turbo")
telegram_agent=TelegramClient(agent)
telegram_agent.run()