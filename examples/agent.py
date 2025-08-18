from aser.agent import Agent
agent=Agent(name="aser agent",description="aser agent",model="gpt-4.1-mini")
response=agent.chat("generate a superman picture")
print(response)