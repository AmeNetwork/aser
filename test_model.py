from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

# client = OpenAI(
#     api_key="",  # Your Anthropic API key
#     base_url="https://api.anthropic.com/v1/"  # Anthropic's API endpoint
# )

# response = client.chat.completions.create(
#     model="claude-3-7-sonnet-20250219", # Anthropic model name
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who are you?"}
#     ],
# )

# print(response.choices[0].message.content)

import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="",
)
message = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)