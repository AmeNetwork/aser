"""
Example: Using Aser with MiniMax models.

MiniMax offers OpenAI-compatible API access to its M2.7 and M2.5 model families,
all featuring 204K-token context windows.

Setup:
  1. Get your API key from https://platform.minimax.io
  2. Set the environment variable:
       export MINIMAX_API_KEY=your_api_key_here
  3. Run this example:
       python examples/agent_minimax.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

from aser.agent import Agent
from aser.providers import MINIMAX, MINIMAX_MODELS

# ---------------------------------------------------------------------------
# Basic usage: use the default MODEL_BASE_URL / MODEL_KEY env vars
# ---------------------------------------------------------------------------
# You can also point MODEL_BASE_URL=https://api.minimax.io/v1 and
# MODEL_KEY=<your MINIMAX_API_KEY> in your .env file and use Agent without
# explicitly passing model_config:
#
#   agent = Agent(name="aser agent", model="MiniMax-M2.7")

# ---------------------------------------------------------------------------
# Explicit usage: pass model_config=MINIMAX
# ---------------------------------------------------------------------------
print("=== MiniMax M2.7 (standard) ===")
agent = Agent(
    name="minimax_agent",
    description="You are a helpful AI assistant powered by MiniMax.",
    model=MINIMAX_MODELS["standard"],   # "MiniMax-M2.7"
    model_config=MINIMAX,               # base_url + MINIMAX_API_KEY
)
response = agent.chat("What is MiniMax AI? Introduce yourself briefly.")
print(response)

# ---------------------------------------------------------------------------
# High-speed variant — same capability, optimised for latency
# ---------------------------------------------------------------------------
print("\n=== MiniMax M2.7-highspeed (fast) ===")
fast_agent = Agent(
    name="minimax_fast_agent",
    description="You are a concise assistant. Always answer in one sentence.",
    model=MINIMAX_MODELS["fast"],       # "MiniMax-M2.7-highspeed"
    model_config=MINIMAX,
)
response = fast_agent.chat("What is the capital of France?")
print(response)

# ---------------------------------------------------------------------------
# Tip: you can also build the config inline without importing MINIMAX
# ---------------------------------------------------------------------------
print("\n=== Inline model_config ===")
inline_agent = Agent(
    name="inline_minimax_agent",
    description="Helpful assistant",
    model="MiniMax-M2.5",
    model_config={
        "base_url": "https://api.minimax.io/v1",
        "api_key": os.getenv("MINIMAX_API_KEY"),
    },
)
response = inline_agent.chat("Say hello in three different languages.")
print(response)
