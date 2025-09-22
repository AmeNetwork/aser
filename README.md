# Aser

Aser is a minimalist, modular, and versatile AI agent framework. You can assemble an agent with just a few lines of code.

![](./examples/images/architecture.png)

[Website](https://ame.network) | [Documentation](https://docs.ame.network/aser/overview) | [Get Support](https://t.me/hello_rickey) | [中文](./README_CN.md)

## Installation

**Install from pypi:**

```bash
pip install aser
```

**Or clone the repository:**

```bash
git clone https://github.com/AmeNetwork/aser.git
cd aser
pip install -r requirements.txt
```

## Set up environment variables

Please refer to `.env.example` file, and create a `.env` file with your own settings. You don't need to configure all environment variables, just select the ones you use.

**.env file example:**

```bash
#MODEL
MODEL_BASE_URL=<your model base url>
MODEL_KEY=<your model key>
```

## Usage

```python
#Basic
from aser.agent import Agent
agent=Agent(name="aser agent",model="gpt-4.1-mini")
response=agent.chat("what's bitcoin?")
print(response)
```

```python
# Full configuration
aser = Agent(
    name="aser",
    model="gpt-4o-mini",
    tools=[web3bio, exa],
    knowledge=knowledge,
    memory=memory,
    chat2web3=[connector],
    mcp=[price],
    trace=trace
)
```

## Get Started

If you clone the project source code, before running the examples, please run `pip install -e .` in the root directory, which allows Python to find and import the aser module from the local source code. If you install it via `pip install aser` , you can run the examples directly.

### Beginner:

- [Aser Agent](./examples/agent.py): Your First AI Agent
- [Model Config](./examples/agent_model.py): Customize the LLM configuration
- [Memory](./examples/agent_memory.py): Build an agent with memory storage
- [RAG](./examples/agent_knowledge.py): Build an agent with knowledge retrieval
- [Tools](./examples/agent_tools.py): Build an agent with tools
- [Toolkits](./examples/agent_toolkits.py): Use built-in toolkits
- [Trace](./examples/agent_trace.py): Build an agent with tracing
- [API](./examples/agent_api.py): Build an agent with API server
- [CLI](./examples/agent_cli.py): Interact with the agent using the CLI
- [Discord](./examples/agent_discord.py): Build an agent with Discord client
- [Telegram](./examples/agent_telegram.py): Build an agent with Telegram client
- [Farcaster](./examples/agent_farcaster.py): Build an agent with Farcaster client

### Intermediate:

- [CoT](./examples/agent_cot.py): Chain of Thought
- [MCP](./examples/agent_mcp.py): Model Context Protocol 
- [Text2SQL](./examples/agent_text2sql.py): Build an agent with Text2SQL
- [Workflow](./examples/agent_workflow.py): Custom Agent Workflows
- [Evaluation](./examples/agent_evaluation.py): Evaluate an AI Agent
- [Router Multi-Agent](./examples/router_multi_agent.py): Multiple agents distribute tasks based on routing
- [Sequential Multi-Agent](./examples/sequential_multi_agent.py): Multiple agents work sequentially
- [Parallel Multi-Agent](./examples/parallel_multi_agent.py): Multiple agents work simultaneously
- [Reactive Multi-Agent](./examples/reactive_multi_agent.py): Multiple agents respond to changes
- [Hierarchical Multi-Agent](./examples/hierarchical_multi_agent.py): Multiple agents work at different levels
- [Agent UI](https://github.com/AmeNetwork/ame-ui): Interact with the agent through the UI

### Advanced:

- [MSCP](./examples/agent_mcp.py): Model Smart Contract Protocol
- [A2Aser](./examples/a2a_server.py): Integrate Google Agent2Agent (A2A) Protocol
- [A2A Client](./examples/a2a_client.py): Agent to Agent Client

### Experiments:
- [ERC8004 Server Agent](./examples/a2a_erc8004_server.py): Server Agent Offers services and executes tasks
- [ERC8004 Identity](./examples/agent_mscp_erc8004.py): Identity registration is performed using the MSCP ERC8004 Connector
