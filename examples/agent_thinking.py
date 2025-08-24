from aser.agent import Agent
agent=Agent(name="aser agent",description="aser agent",model="gpt-4.1-mini")
result=agent.thinking("Calculate (100-10) * 3 +(100/2)")
print(result)
