# Aser

Aser 是一个极简、模块化且多功能的 AI Agent 框架。只需几行代码即可组装一个智能体。

![](./examples/images/architecture.png)

[官网](https://ame.network) | [文档](https://docs.ame.network/aser/overview) | [获取支持](https://t.me/hello_rickey) | [English](./README.md)

## 安装

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

## 设置环境变量

请参考 `.env.example` 文件，并根据您的需求创建 `.env` 文件。无需配置所有环境变量，只需选择您需要使用的即可。

**.env 文件示例：**

```bash
#MODEL
MODEL_BASE_URL=<你的模型基础地址>
MODEL_KEY=<你的模型密钥>
```

## 用法

```python
# 基础用法
from aser.agent import Agent
agent = Agent(name="aser agent", model="gpt-4.1-mini")
response = agent.chat("什么是比特币？")
print(response)
```

```python
# 完整配置
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

## 快速开始

如果您是通过克隆项目源码的方式安装，在运行示例前请先在根目录执行 `pip install -e .`，这样 Python 能够从本地源码导入 aser 模块。如果通过 `pip install aser` 安装，则可直接运行示例。

### 入门：

- [Aser Agent](./examples/agent.py)：你的第一个 AI Agent
- [Model Config](./examples/agent_model.py)：自定义 LLM 配置
- [Memory](./examples/agent_memory.py)：构建带有记忆存储的智能体
- [RAG](./examples/agent_knowledge.py)：构建具备知识检索的智能体
- [Tools](./examples/agent_tools.py)：构建带有工具的智能体
- [Toolkits](./examples/agent_toolkits.py)：使用内置工具包
- [Trace](./examples/agent_trace.py)：构建带有追踪功能的智能体
- [API](./examples/agent_api.py)：构建带有 API 服务的智能体
- [CLI](./examples/agent_cli.py)：通过 CLI 与智能体交互
- [Discord](./examples/agent_discord.py)：构建带有 Discord 客户端的智能体
- [Telegram](./examples/agent_telegram.py)：构建带有 Telegram 客户端的智能体
- [Farcaster](./examples/agent_farcaster.py)：构建带有 Farcaster 客户端的智能体

### 进阶：

- [CoT](./examples/agent_cot.py)：思维链
- [MCP](./examples/agent_mcp.py)：模型上下文协议
- [Text2SQL](./examples/agent_text2sql.py): 构建一个带有Text2SQL的代理
- [Workflow](./examples/agent_workflow.py)：自定义智能体工作流
- [Evaluation](./examples/agent_evaluation.py)：评估 AI Agent
- [Router Multi-Agent](./examples/router_multi_agent.py)：多智能体根据路由分配任务
- [Sequential Multi-Agent](./examples/sequential_multi_agent.py)：多智能体顺序协作
- [Parallel Multi-Agent](./examples/parallel_multi_agent.py)：多智能体并行协作
- [Reactive Multi-Agent](./examples/reactive_multi_agent.py)：多智能体响应变化
- [Hierarchical Multi-Agent](./examples/hierarchical_multi_agent.py)：多智能体分层协作
- [Agent UI](https://github.com/AmeNetwork/ame-ui)：通过 UI 与智能体交互

### 高级：

- [MSCP](https://github.com/AmeNetwork/Model-Smart-Contract-Protocol)：模型智能合约协议
- [A2Aser](./examples/a2a.py)：集成 Google Agent2Agent (A2A) 协议
- [A2A Client](./examples/a2a_client.py)：Agent to Agent 客户端