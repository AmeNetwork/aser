from aser.agent import Agent
# openai 
openai_agent=Agent(name="aser agent",description="aser agent",model="openai/gpt-4.1-mini")
openai_agent_response=openai_agent.chat("what's openai_agent model? max 100 words")
print("openai:",openai_agent_response)

# deepseek 
deepseek_agent=Agent(name="aser agent",description="aser agent",model="deepseek/deepseek-chat-v3.1:free")
deepseek_agent_response=deepseek_agent.chat("what's deepseek? max 100 words")
print("deepseek:",deepseek_agent_response)

# qwen 
qwen_agent=Agent(name="aser agent",description="aser agent",model="qwen/qwen3-coder:free")
qwen_agent_response=qwen_agent.chat("what's qwen model? max 100 words")
print("qwen:",qwen_agent_response)
