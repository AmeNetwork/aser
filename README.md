# Aser

Aser is equipped with standardized AI capability middleware, such as knowledge, memory, tracing, CoT, API interfaces, and social clients. By dynamically integrating Web3 toolkits, it helps developers quickly build and launch AI agents with native Web3 capabilities.

![](./examples/images/architecture.png)

[Website](https://ame.network) | [Documentation](https://docs.ame.network/aser/overview) | [Get Support](https://t.me/hello_rickey)  | [中文](./README_CN.md) 

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
MODEL_BASE_URL=https://openrouter.ai/api/v1
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
Your First AI Agent [example](./examples/agent.py)

Create an AI Agent with Model Config [example](./examples/agent_model.py)

Create an AI Agent with Memory [example](./examples/agent_memory.py)

Create an AI Agent with Knowledge [example](./examples/agent_knowledge.py)     

Create an AI Agent with Tools [example](./examples/agent_tools.py)  

Create an AI Agent with Toolkits [example](./examples/agent_toolkits.py)

Create an AI Agent with Trace [example](./examples/agent_trace.py)

Create an AI Agent Server [example](./examples/agent_api.py)

Create an AI Agent with CLI [example](./examples/agent_cli.py)

Create a Discord AI Agent [example](./examples/agent_discord.py)

Create a Telegram AI Agent [example](./examples/agent_telegram.py)

Create a Farcaster AI Agent [example](./examples/agent_farcaster.py)

### Intermediate:

Create an AI Agent with Chain of Thought [example](./examples/agent_cot.py)

Create an AI Agent with MCP [example](./examples/agent_mcp.py)

Create an AI Agent with Workflow [example](./examples/agent_workflow.py)

Create an AI Agent with UI [example](https://github.com/AmeNetwork/ame-ui)

Evaluate an AI Agent [example](./examples/agent_evaluation.py)

Router Multi-Agents [example](./examples/router_multi_agents.py)

Sequential Multi-Agents [example](./examples/sequential_multi_agents.py)

Parallel Multi-Agents [example](./examples/parallel_multi_agents.py)

Reactive Multi-Agents [example](./examples/reactive_multi_agents.py)

Hierarchical Multi-Agents [example](./examples/hierarchical_multi_agents.py)


### Advanced:

Create an AI Agent with Model Smart Contract Protocol [example](https://github.com/AmeNetwork/Model-Smart-Contract-Protocol)