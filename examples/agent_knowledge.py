from aser.agent import Agent
from aser.knowledge import Knowledge

knowledge = Knowledge(name="aser_knowledge", query_ns=2)

knowledge.knowledger_from_file("README.md")

agent = Agent(
    name="aser agent",
    model="gpt-4.1-mini",
    knowledge=knowledge,
)
response = agent.chat("what is aser agent?")
print(response)
