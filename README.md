# Aser

> [!Warning]  
> Aser does not issue any tokens!

Aser is equipped with standardized AI capability middleware, such as knowledge, memory, tracing, thinking, API interfaces, and social clients. By dynamically integrating Web3 toolkits, it helps developers quickly build and launch AI agents with native Web3 capabilities.

![](./examples/images/architecture.png)

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

## Examples

[Create a simple AI Agent](./examples/agent.py)

[Create Discord AI Agent](./examples/agent_discord.py)

[Create Telegram AI Agent](./examples/agent_telegram.py)

[Create Farcaster AI Agent](./examples/agent_farcaster.py)

[Create an AI Agent with Memory](./examples/agent_memory.py)

[Create an AI Agent with Knowledge](./examples/agent_knowledge.py)

[Create an AI Agent with Tools](./examples/agent_tools.py)  

[Create an AI Agent with Toolkits](./examples/agent_toolkits.py)

[Create an AI Agent with Trace](./examples/agent_trace.py)

[Create an AI Agent with Model Smart Contract Protocol](./examples/agent_mscp.py)

[Create an AI Agent Server](./examples/agent_server.py)

[Create an AI Agent with Cli](./examples/agent_cli.py)

[Create an AI Agent with Thinking](./examples/agent_thinking.py)

[Integrate Swarms](./examples/aser_swarms.py)

