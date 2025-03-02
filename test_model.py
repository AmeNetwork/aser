from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key="",  # Your Anthropic API key
    base_url=""  # Anthropic's API endpoint
)

completion = client.chat.completions.create(
  extra_body={},
  model="google/gemini-2.0-flash-lite-001",
  messages=[
    {
      "role": "user",
      "content": "Hello"
    }
  ]
)
print(completion.choices[0].message.content)
