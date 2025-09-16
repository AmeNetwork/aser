from aser.agent import Agent
from aser.cot import CoT
agent=Agent(name="aser agent",description="aser agent",model="gpt-4.1-mini")
cot=CoT(agent)
result=cot.thinking("Calculate (100-10) * 3 +(100/2)")
cot.print_steps(result)
