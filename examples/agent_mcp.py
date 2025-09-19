from aser.agent import Agent
from aser.mcp import MCP
weather_mcp=MCP("http://127.0.0.1:9000/mcp") 
agent = Agent(name="aser agent", description="aser agent", model="gpt-4.1-mini", mcp=[weather_mcp])
response =agent.chat("get the weather of NewYork")
print(response)



