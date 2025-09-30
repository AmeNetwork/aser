from aser.agent import Agent
from aser.evolution import SelfCodingTool
tool_creator = Agent(
    name="tool_creator",
    model="gpt-4.1-mini",
    description="""
            You are a Tool creation expert. Create Python functions based on user requirements.
            Requirements: safe code, error handling, documentation strings.
            """
)
self_coding_tool = SelfCodingTool(tool_creator)

new_tool = self_coding_tool.create_tool(
    "read a github readme file by url, such as https://github.com/AmeNetwork/aser/blob/main/README.md")

agent = Agent(name="aser agent", description="aser agent",
              model="gpt-4.1-mini",
              tools=[new_tool])

response = agent.chat(
    "read the readme file of https://github.com/AmeNetwork/aser/blob/main/README.md")

print(response)
