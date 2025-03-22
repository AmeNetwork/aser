from amer.agent import Agent
agent=Agent(name="amer agent",description="amer agent",model="gpt-3.5-turbo")
response=agent.chat("What is Bitcoin?")
print(response)