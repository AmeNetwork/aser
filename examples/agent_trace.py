from amer.trace import Trace
from amer.agent import Agent
trace=Trace(session=1)
agent=Agent(name="amer agent",description="amer agent",model="gpt-3.5-turbo",trace=trace)
response=agent.chat("what is bitcoin?")
