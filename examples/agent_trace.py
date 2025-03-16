from esper.trace import Trace
from esper.agent import Agent
trace=Trace(session=1)
agent=Agent(name="esper agent",description="esper agent",model="gpt-3.5-turbo",trace=trace)
response=agent.chat("what is bitcoin?")
