from aser.trace import Trace
from aser.agent import Agent
trace=Trace(session=1)
agent=Agent(name="aser agent",description="aser agent",model="gpt-3.5-turbo",trace=trace)
response=agent.chat("what is bitcoin?")
