# Aser

Aser is a minimalist, modular, and versatile AI agent framework. You can assemble an agent with just a few lines of code.

![](./examples/images/architecture.png)

[Twitter](https://x.com/Web3Rickey) | [Documentation](https://docs.ame.network/aser/overview) | [Get Support](https://t.me/hello_rickey) | [中文](./README_CN.md)

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

## Supported LLM Providers

Aser works with any OpenAI-compatible API. Use the built-in `providers` module for quick setup:

| Provider | Models | Context |
|----------|--------|---------|
| OpenAI | gpt-4o, gpt-4.1-mini, … | up to 128K |
| [MiniMax](https://platform.minimax.io) | MiniMax-M2.7, MiniMax-M2.7-highspeed, MiniMax-M2.5, MiniMax-M2.5-highspeed | **204K** |
| Any OpenAI-compat API | set `MODEL_BASE_URL` + `MODEL_KEY` | depends on model |

### Using MiniMax

```bash
export MINIMAX_API_KEY=your_api_key_here
```

```python
from aser.agent import Agent
from aser.providers import MINIMAX, MINIMAX_MODELS

agent = Agent(
    name="minimax_agent",
    model=MINIMAX_MODELS["standard"],   # "MiniMax-M2.7"
    model_config=MINIMAX,
)
response = agent.chat("What is MiniMax AI?")
print(response)
```

See the full example at [examples/agent_minimax.py](./examples/agent_minimax.py).

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
- [MiniMax](./examples/agent_minimax.py): Use MiniMax M2.7 / M2.5 models (204K context)
- [Character](./examples/agent_character.py): Build an agent with character
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
- [Parallel Search MCP](./examples/parallel-search.md): Free web search and page fetching
- [Local code MCP](./examples/sem-code.md): Read-only entity lookup through a self-hosted Sem HTTP preview
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
- [Self-Coding Tool](./examples/self_coding_tool.py): Agent can self-code to build tools

### Experiments:
- [ERC8004 Server Agent](./examples/a2a_erc8004_server.py): Server Agent Offers services and executes tasks
- [ERC8004 Identity](./examples/agent_mscp_erc8004.py): Identity registration is performed using the MSCP ERC8004 Connector


## License
Aser is open-source and licensed under the MIT License.


![](./examples/images/star.png)
