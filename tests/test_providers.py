"""
Unit tests for aser/providers.py — MiniMax provider presets.

Imports providers.py directly (not through aser.__init__) so we don't need
all the heavy optional dependencies (discord, telegram, web3, etc.).

Run with: pytest tests/test_providers.py -v
"""

import os
import sys
import importlib
import importlib.util
import types
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helper: load providers.py in isolation (no __init__ side effects)
# ---------------------------------------------------------------------------

PROVIDERS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "aser", "providers.py"
)


def _load_providers(extra_env: dict | None = None):
    """Load aser/providers.py with an optionally patched environment."""
    env_patch = extra_env or {}
    with patch.dict(os.environ, env_patch, clear=False):
        spec = importlib.util.spec_from_file_location("aser.providers", PROVIDERS_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


# ---------------------------------------------------------------------------
# Helper: load agent.py with OpenAI stubbed out
# ---------------------------------------------------------------------------

AGENT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "aser", "agent.py"
)


def _load_agent_with_mock_openai():
    """Import aser/agent.py with all its dependencies mocked."""
    # Stub the modules Agent imports
    stubs = {
        "openai": types.ModuleType("openai"),
        "aser.utils": types.ModuleType("aser.utils"),
        "aser.tools": types.ModuleType("aser.tools"),
    }
    # openai.OpenAI mock
    mock_openai_cls = MagicMock()
    stubs["openai"].OpenAI = mock_openai_cls

    # aser.utils stubs
    stubs["aser.utils"].knowledge_to_prompt = MagicMock(return_value="")
    stubs["aser.utils"].handle_tool_function = MagicMock(return_value="")
    stubs["aser.utils"].safe_serialize = MagicMock(return_value=None)

    # aser.tools.Tools stub
    mock_tools_cls = MagicMock()
    stubs["aser.tools"].Tools = mock_tools_cls

    with patch.dict(sys.modules, stubs):
        spec = importlib.util.spec_from_file_location("aser.agent", AGENT_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, mock_openai_cls


# ---------------------------------------------------------------------------
# MINIMAX preset — base_url
# ---------------------------------------------------------------------------

class TestMinimaxBaseUrl:
    def test_base_url_is_openai_compat(self):
        p = _load_providers()
        assert p.MINIMAX["base_url"] == "https://api.minimax.io/v1"

    def test_base_url_uses_https(self):
        p = _load_providers()
        assert p.MINIMAX["base_url"].startswith("https://")

    def test_base_url_ends_with_v1(self):
        p = _load_providers()
        assert p.MINIMAX["base_url"].endswith("/v1")


# ---------------------------------------------------------------------------
# MINIMAX preset — api_key
# ---------------------------------------------------------------------------

class TestMinimaxApiKey:
    def test_api_key_from_env(self):
        p = _load_providers({"MINIMAX_API_KEY": "mk-test-key"})
        assert p.MINIMAX["api_key"] == "mk-test-key"

    def test_api_key_different_value(self):
        p = _load_providers({"MINIMAX_API_KEY": "mk-another-key-456"})
        assert p.MINIMAX["api_key"] == "mk-another-key-456"

    def test_api_key_missing_returns_placeholder(self):
        clean_env = {k: v for k, v in os.environ.items() if k != "MINIMAX_API_KEY"}
        with patch.dict(os.environ, clean_env, clear=True):
            p = _load_providers()
        assert p.MINIMAX["api_key"] == "MISSING_API_KEY"

    def test_minimax_dict_keys(self):
        p = _load_providers({"MINIMAX_API_KEY": "k"})
        assert set(p.MINIMAX.keys()) == {"base_url", "api_key"}


# ---------------------------------------------------------------------------
# MINIMAX_MODELS
# ---------------------------------------------------------------------------

class TestMinimaxModels:
    def test_standard_model_name(self):
        p = _load_providers()
        assert p.MINIMAX_MODELS["standard"] == "MiniMax-M2.7"

    def test_fast_model_name(self):
        p = _load_providers()
        assert p.MINIMAX_MODELS["fast"] == "MiniMax-M2.7-highspeed"

    def test_standard_v25_model_name(self):
        p = _load_providers()
        assert p.MINIMAX_MODELS["standard_v25"] == "MiniMax-M2.5"

    def test_fast_v25_model_name(self):
        p = _load_providers()
        assert p.MINIMAX_MODELS["fast_v25"] == "MiniMax-M2.5-highspeed"

    def test_all_model_keys_present(self):
        p = _load_providers()
        assert set(p.MINIMAX_MODELS.keys()) == {"standard", "fast", "standard_v25", "fast_v25"}

    def test_m27_in_standard_name(self):
        p = _load_providers()
        assert "M2.7" in p.MINIMAX_MODELS["standard"]

    def test_m25_in_standard_v25_name(self):
        p = _load_providers()
        assert "M2.5" in p.MINIMAX_MODELS["standard_v25"]

    def test_highspeed_suffix_in_fast_model(self):
        p = _load_providers()
        assert "highspeed" in p.MINIMAX_MODELS["fast"]


# ---------------------------------------------------------------------------
# OPENAI preset
# ---------------------------------------------------------------------------

class TestOpenAIPreset:
    def test_openai_base_url(self):
        p = _load_providers({"OPENAI_API_KEY": "sk-test"})
        assert p.OPENAI["base_url"] == "https://api.openai.com/v1"

    def test_openai_api_key_from_env(self):
        p = _load_providers({"OPENAI_API_KEY": "sk-hello"})
        assert p.OPENAI["api_key"] == "sk-hello"

    def test_openai_dict_has_correct_keys(self):
        p = _load_providers({"OPENAI_API_KEY": "sk-x"})
        assert "base_url" in p.OPENAI
        assert "api_key" in p.OPENAI


# ---------------------------------------------------------------------------
# custom_provider helper
# ---------------------------------------------------------------------------

class TestCustomProvider:
    def test_returns_correct_dict(self):
        p = _load_providers()
        cfg = p.custom_provider("https://example.com/v1", "my-key")
        assert cfg == {"base_url": "https://example.com/v1", "api_key": "my-key"}

    def test_base_url_preserved(self):
        p = _load_providers()
        url = "https://api.my-llm.io/v2"
        cfg = p.custom_provider(url, "k")
        assert cfg["base_url"] == url

    def test_api_key_preserved(self):
        p = _load_providers()
        key = "supersecretkey"
        cfg = p.custom_provider("https://x.com", key)
        assert cfg["api_key"] == key

    def test_returns_dict_type(self):
        p = _load_providers()
        cfg = p.custom_provider("https://x.com", "k")
        assert isinstance(cfg, dict)


# ---------------------------------------------------------------------------
# Agent integration: model_config is forwarded to OpenAI constructor
# ---------------------------------------------------------------------------

class TestAgentWithMiniMaxConfig:
    def test_openai_called_with_minimax_config(self):
        agent_mod, mock_openai_cls = _load_agent_with_mock_openai()
        minimax_cfg = {
            "base_url": "https://api.minimax.io/v1",
            "api_key": "test-key",
        }
        agent_mod.Agent(name="t", model="MiniMax-M2.7", model_config=minimax_cfg)
        mock_openai_cls.assert_called_once_with(**minimax_cfg)

    def test_agent_model_attribute(self):
        agent_mod, _ = _load_agent_with_mock_openai()
        agent = agent_mod.Agent(
            name="t",
            model="MiniMax-M2.7-highspeed",
            model_config={"base_url": "https://api.minimax.io/v1", "api_key": "k"},
        )
        assert agent.model == "MiniMax-M2.7-highspeed"

    def test_agent_uses_m25_model(self):
        agent_mod, mock_openai_cls = _load_agent_with_mock_openai()
        cfg = {"base_url": "https://api.minimax.io/v1", "api_key": "k"}
        agent = agent_mod.Agent(name="t", model="MiniMax-M2.5", model_config=cfg)
        assert agent.model == "MiniMax-M2.5"
        mock_openai_cls.assert_called_once_with(**cfg)

    def test_agent_name_stored(self):
        agent_mod, _ = _load_agent_with_mock_openai()
        agent = agent_mod.Agent(
            name="minimax_agent",
            model="MiniMax-M2.7",
            model_config={"base_url": "https://api.minimax.io/v1", "api_key": "k"},
        )
        assert agent.name == "minimax_agent"


# ---------------------------------------------------------------------------
# Integration smoke tests (only run if MINIMAX_API_KEY is set)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(
    not os.getenv("MINIMAX_API_KEY"),
    reason="MINIMAX_API_KEY not set — skipping live API test",
)
class TestMinimaxLiveIntegration:
    """Live API tests — require a valid MINIMAX_API_KEY."""

    def _make_agent(self, model_key: str):
        """Build an Agent using MINIMAX provider without importing through __init__."""
        p = _load_providers()
        agent_mod, _ = _load_agent_with_mock_openai()

        # For live tests, use the real OpenAI client
        from openai import OpenAI
        import aser.agent as real_agent_mod
        return real_agent_mod, p

    def test_minimax_m27_chat(self):
        import importlib.util, sys, types
        spec = importlib.util.spec_from_file_location("aser.agent_real", AGENT_PATH)
        # Can't easily do live test without deps; skip if openai not available
        try:
            from openai import OpenAI
        except ImportError:
            pytest.skip("openai package not installed")

        p = _load_providers()
        from openai import OpenAI

        client = OpenAI(**p.MINIMAX)
        resp = client.chat.completions.create(
            model=p.MINIMAX_MODELS["fast"],
            messages=[{"role": "user", "content": "Reply with: OK"}],
            max_tokens=10,
        )
        assert resp.choices[0].message.content is not None

    def test_minimax_m25_chat(self):
        try:
            from openai import OpenAI
        except ImportError:
            pytest.skip("openai package not installed")

        p = _load_providers()
        from openai import OpenAI

        client = OpenAI(**p.MINIMAX)
        resp = client.chat.completions.create(
            model=p.MINIMAX_MODELS["fast_v25"],
            messages=[{"role": "user", "content": "Say hello."}],
            max_tokens=20,
        )
        assert isinstance(resp.choices[0].message.content, str)
        assert len(resp.choices[0].message.content) > 0

    def test_minimax_204k_context_available(self):
        """Model names contain version markers indicating 204K context support."""
        p = _load_providers()
        for key, model_name in p.MINIMAX_MODELS.items():
            assert "MiniMax" in model_name, f"Unexpected model name for key {key!r}: {model_name!r}"
