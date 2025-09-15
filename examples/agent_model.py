from aser.agent import Agent
from dotenv import load_dotenv
import os
load_dotenv()

# default model config 
openai_agent=Agent(name="aser agent",description="aser agent",model="openai/gpt-4.1-mini")
openai_agent_response=openai_agent.chat("what's openai_agent model? max 100 words")
print("openai:",openai_agent_response)

# custom model config 
qwen_agent=Agent(name="aser agent",description="aser agent",model="qwen/qwen3-coder:free",model_config={
    "base_url": os.getenv("QWEN_BASE_URL"),
    "api_key": os.getenv("QWEN_KEY"),
})
qwen_agent_response=qwen_agent.chat("what's qwen model? max 100 words")
print("qwen:",qwen_agent_response)
