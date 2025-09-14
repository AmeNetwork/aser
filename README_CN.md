# Aser

Aser 配备了标准化的 AI 能力中间件，如知识、记忆、追踪、思考、API 接口和社交客户端。通过动态集成 Web3 工具包，帮助开发者快速构建并发布具备原生 Web3 能力的 AI Agent。

![](./examples/images/architecture.png)

[官方网站](https://ame.network) | [文档](https://docs.ame.network/aser/overview) | [获取支持](https://t.me/hello_rickey)

## 安装方法

**通过 pypi 安装：**
```bash
pip install aser
```

**或克隆仓库：**
```bash
git clone https://github.com/AmeNetwork/aser.git
cd aser
pip install -r requirements.txt
```

## 环境变量设置

请参考 `.env.example` 文件，并根据自己的需求创建 `.env` 文件。无需配置所有环境变量，只需选择需要使用的部分。

**.env 文件示例：**
```bash
#OPENAI
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_KEY=<你的 openai key>
```

## 基本用法
```python
from aser.agent import Agent
agent=Agent(name="aser agent",model="gpt-4.1-mini")
response=agent.chat("what's bitcoin?")
print(response)
```

## 集成与示例

创建 Discord AI Agent [示例](./examples/agent_discord.py)

创建 Telegram AI Agent [示例](./examples/agent_telegram.py)

创建 Farcaster AI Agent [示例](./examples/agent_farcaster.py)

创建具备记忆的 AI Agent [示例](./examples/agent_memory.py)

创建具备知识的 AI Agent [示例](./examples/agent_knowledge.py)

创建具备工具的 AI Agent [示例](./examples/agent_tools.py)

创建具备工具包的 AI Agent [示例](./examples/agent_toolkits.py)

创建具备追踪的 AI Agent [示例](./examples/agent_trace.py)

创建具备模型智能合约协议的 AI Agent [示例](./examples/agent_mscp.py)

创建 AI Agent 服务器 [示例](./examples/agent_api.py)

创建具备命令行的 AI Agent [示例](./examples/agent_cli.py)

创建具备思考能力的 AI Agent [示例](./examples/agent_thinking.py)

创建具备群体协作的 AI Agent [示例](./examples/aser_swarms.py)

创建具备 MCP 的 AI Agent [示例](./examples/agent_mcp.py)

创建具备工作流的 AI Agent [示例](./examples/agent_workflow.py)

创建具备 UI 的 AI Agent [示例](https://github.com/AmeNetwork/ame-ui)