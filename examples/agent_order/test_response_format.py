from aser.agent import Agent
from pydantic import BaseModel
import json

class CheckWork(BaseModel):
    verify:bool

agent=Agent(name="api-agent",model="gpt-4o-mini")
response=agent.chat("1==1吗",response_format=CheckWork)
print("response:",json.loads(response)["verify"])