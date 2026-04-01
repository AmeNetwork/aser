"""
Provider presets for popular LLM APIs.

Usage:
    from aser.providers import MINIMAX, OPENAI
    from aser.agent import Agent

    agent = Agent(name="my_agent", model="MiniMax-M2.7", model_config=MINIMAX)
"""

import os


def _make_config(base_url: str, api_key_env: str, api_key: str | None = None) -> dict:
    return {
        "base_url": base_url,
        "api_key": api_key or os.getenv(api_key_env) or "MISSING_API_KEY",
    }


# ---------------------------------------------------------------------------
# MiniMax — OpenAI-compatible endpoint
# Models: MiniMax-M2.7, MiniMax-M2.7-highspeed, MiniMax-M2.5, MiniMax-M2.5-highspeed
# Context: 204K tokens for all models
# Docs: https://docs.minimax.io
# Note: temperature must be in (0.0, 1.0]; do NOT use temperature=0
# ---------------------------------------------------------------------------
MINIMAX = _make_config(
    base_url="https://api.minimax.io/v1",
    api_key_env="MINIMAX_API_KEY",
)

# Recommended models
MINIMAX_MODELS = {
    "standard": "MiniMax-M2.7",
    "fast": "MiniMax-M2.7-highspeed",
    "standard_v25": "MiniMax-M2.5",
    "fast_v25": "MiniMax-M2.5-highspeed",
}

# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------
OPENAI = _make_config(
    base_url="https://api.openai.com/v1",
    api_key_env="OPENAI_API_KEY",
)

# ---------------------------------------------------------------------------
# Anthropic (OpenAI-compatible proxy via third-party gateways)
# Use your gateway's base_url; Anthropic's native API is not OpenAI-compatible.
# ---------------------------------------------------------------------------
ANTHROPIC_COMPAT = _make_config(
    base_url=os.getenv("ANTHROPIC_COMPAT_BASE_URL", "https://api.anthropic.com/v1"),
    api_key_env="ANTHROPIC_API_KEY",
)

# ---------------------------------------------------------------------------
# Generic helper: build a custom provider config on the fly
# ---------------------------------------------------------------------------
def custom_provider(base_url: str, api_key: str) -> dict:
    """Return a model_config dict for any OpenAI-compatible provider."""
    return {"base_url": base_url, "api_key": api_key}
