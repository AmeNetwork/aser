from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=""
)

completion = client.chat.completions.create(
  extra_body={},
  model="anthropic/claude-3.7-sonnet",
  messages=[
    {
      "role": "user",
      "content":"Hello Claude"
    }
  ]
)
print(completion)