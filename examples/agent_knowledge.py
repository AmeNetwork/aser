from aser.agent import Agent
from aser.knowledge import Knowledge

knowledge = Knowledge(name="CryptoHistory", query_ns=1)
knowledge_data = [
    {
        "id": "1",
        "document": "Ethereum is a decentralized blockchain with smart contract functionality.",
        "metadata": {"founder": "Vitalik Buterin", "token": "ETH", "year": 2013},
    },
    {
        "id": "2",
        "document": "Bitcoin is a decentralized digital currency.",
        "metadata": {"founder": "Satoshi Nakamoto", "token": "BTC", "year": 2009},
    },
    {
        "id": "3",
        "document": "Binance is a cryptocurrency exchange.",
        "metadata": {"founder": "CZ", "token": "BNB", "year": 2017},
    },
]
knowledge.upsert(knowledge_data)
agent = Agent(
    name="aser agent",
    description="aser agent",
    model="gpt-3.5-turbo",
    knowledge=knowledge,
)
response = agent.chat("what is Ethereum?")
