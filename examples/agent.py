from aser.agent import Agent
agent=Agent(name="aser agent",description="aser agent",model="gpt-3.5-turbo")
response=agent.chat("What is Bitcoin?")
print(response)