from aser.toolkits import exa
from aser.agent import Agent
agent=Agent(name="aser agent",description="aser agent",model="gpt-4.1-mini",tools=[exa])
response=agent.chat("search for latest research in LLMs ")
print(response)