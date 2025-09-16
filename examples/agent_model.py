from aser.agent import Agent
from dotenv import load_dotenv
import os
load_dotenv()

# custom model config 
qwen_agent=Agent(name="aser agent",description="aser agent",model="qwen/qwen3-coder:free",model_config={
    "base_url": os.getenv("QWEN_BASE_URL"),
    "api_key": os.getenv("QWEN_KEY"),
})
qwen_agent_response=qwen_agent.chat("what's qwen model? max 100 words")
print("qwen:",qwen_agent_response)
