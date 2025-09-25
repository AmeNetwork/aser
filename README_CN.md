# Aser

Aser 是一个极简、模块化且多功能的 AI Agent 框架。你只需几行代码即可组装一个智能体。

![](./examples/images/architecture.png)

[推特](https://x.com/Web3Rickey) | [文档](https://docs.ame.network/aser/overview) | [获取支持](https://t.me/hello_rickey) | [English](./README.md)

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

请参考 `.env.example` 文件，并根据你的配置创建 `.env` 文件。无需配置所有环境变量，只需选择你需要的即可。

**.env 文件示例：**

```bash
#MODEL
MODEL_BASE_URL=<你的模型基础地址>
MODEL_KEY=<你的模型密钥>
```

## 用法示例

```python
# 基础用法
from aser.agent import Agent
agent=Agent(name="aser agent",model="gpt-4.1-mini")
response=agent.chat("什么是比特币？")
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

如果你是通过克隆源码安装，在运行示例前请在根目录执行 `pip install -e .`，这样 Python 能够从本地源码导入 aser 模块。如果通过 `pip install aser` 安装，可直接运行示例。

### 入门示例：

- [Aser Agent](./examples/agent.py)：你的第一个 AI Agent
- [模型配置](./examples/agent_model.py)：自定义 LLM 配置
- [记忆存储](./examples/agent_memory.py)：构建带记忆的智能体
- [知识检索](./examples/agent_knowledge.py)：构建带知识检索的智能体
- [工具集成](./examples/agent_tools.py)：集成工具
- [内置工具包](./examples/agent_toolkits.py)：使用内置工具包
- [追踪功能](./examples/agent_trace.py)：构建带追踪的智能体
- [API 服务](./examples/agent_api.py)：构建 API 服务智能体
- [命令行交互](./examples/agent_cli.py)：通过 CLI 交互
- [Discord 集成](./examples/agent_discord.py)：集成 Discord 客户端
- [Telegram 集成](./examples/agent_telegram.py)：集成 Telegram 客户端
- [Farcaster 集成](./examples/agent_farcaster.py)：集成 Farcaster 客户端

### 进阶示例：

- [CoT](./examples/agent_cot.py)：思维链
- [MCP](./examples/agent_mcp.py)：模型上下文协议
- [Text2SQL](./examples/agent_text2sql.py)：文本转 SQL 智能体
- [自定义工作流](./examples/agent_workflow.py)：自定义智能体工作流
- [智能体评估](./examples/agent_evaluation.py)：评估 AI Agent
- [路由多智能体](./examples/router_multi_agent.py)：多智能体任务分发
- [顺序多智能体](./examples/sequential_multi_agent.py)：多智能体顺序协作
- [并行多智能体](./examples/parallel_multi_agent.py)：多智能体并行协作
- [响应式多智能体](./examples/reactive_multi_agent.py)：多智能体响应变化
- [分层多智能体](./examples/hierarchical_multi_agent.py)：多智能体分层协作
- [Agent UI](https://github.com/AmeNetwork/ame-ui)：通过 UI 交互

### 高级示例：

- [MSCP](./examples/agent_mcp.py)：模型智能合约协议
- [A2Aser](./examples/a2a_server.py)：集成 Google Agent2Agent (A2A) 协议
- [A2A 客户端](./examples/a2a_client.py)：Agent 间通信客户端

### 实验性功能：
- [ERC8004 服务智能体](./examples/a2a_erc8004_server.py)：服务智能体提供服务并执行任务
- [ERC8004 身份](./examples/agent_mscp_erc8004.py)：通过 MSCP ERC8004 连接器进行身份注册

## 许可证
Aser 是开源项目，采用 MIT 许可证。

![](./examples/images/star.png)