# Aser

Aser is equipped with standardized AI capability middleware, such as knowledge, memory, tracing, thinking, API interfaces, and social clients. By dynamically integrating Web3 toolkits, it helps developers quickly build and launch AI agents with native Web3 capabilities.

![](./examples/images/architecture.png)

[Website](https://ame.network) | [Documentation](https://docs.ame.network/aser/overview) | [Get Support](https://t.me/hello_rickey) 

## Installation

**Install from pypi:**

```bash
pip3 install aser
```

**Clone the repository:**

```bash
git clone https://github.com/AmeNetwork/aser.git
cd aser
pip3 install -r requirements.txt
```

## Set up environment variables

Please refer to `.env.example` file, and create a `.env` file with your own settings. You can use two methods to import environment variables.

**Using python-dotenv:**

```bash
pip install python-dotenv
```

Then add the following code to your python file.

```python
from dotenv import load_dotenv
load_dotenv()
```

**Exporting all variables in the terminal:**

```bash
export $(grep -v '^#' .env | xargs)
```
## Basic Usage
```python
from aser.agent import Agent
agent=Agent(name="aser agent",model="gpt-4.1-mini")
response=agent.chat("what's bitcoin?")
print(response)
```

## Integrations & Examples

Create a Discord AI Agent [example](./examples/agent_discord.py)

Create a Telegram AI Agent [example](./examples/agent_telegram.py)

Create a Farcaster AI Agent [example](./examples/agent_farcaster.py)

Create an AI Agent with Memory [example](./examples/agent_memory.py)

Create an AI Agent with Knowledge [example](./examples/agent_knowledge.py)          

Create an AI Agent with Tools [example](./examples/agent_tools.py)  

Create an AI Agent with Toolkits [example](./examples/agent_toolkits.py)

Create an AI Agent with Trace [example](./examples/agent_trace.py)

Create an AI Agent with Model Smart Contract Protocol [example](./examples/agent_mscp.py)

Create an AI Agent Server [example](./examples/agent_server.py)

Create an AI Agent with CLI [example](./examples/agent_cli.py)

Create an AI Agent with Thinking [example](./examples/agent_thinking.py)

Create an AI Agent with Swarms [example](./examples/aser_swarms.py)

Create an AI Agent with MCP [example](./examples/agent_mcp.py)

Create an AI Agent with Workflow [example](./examples/agent_workflow.py)

Create an AI Agent with UI [example](https://github.com/AmeNetwork/ame-ui)

