import unittest
from unittest.mock import patch

from aser.mcp import MCP


class FakeClient:
    def __init__(self, transport):
        self.transport = transport

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


class MCPTransportTests(unittest.TestCase):
    def test_headers_and_auth_reach_their_transport_parameters(self):
        headers = {"User-Agent": "aser-parallel-search-example/0.1.9"}
        with patch("aser.mcp.StreamableHttpTransport") as transport:
            with patch("aser.mcp.Client", FakeClient):
                MCP("https://search.parallel.ai/mcp", auth="token", header=headers)
        transport.assert_called_once_with(
            "https://search.parallel.ai/mcp", headers=headers, auth="token"
        )

    def test_anonymous_default_is_preserved(self):
        with patch("aser.mcp.StreamableHttpTransport") as transport:
            with patch("aser.mcp.Client", FakeClient):
                MCP("http://127.0.0.1:9000/mcp")
        transport.assert_called_once_with(
            "http://127.0.0.1:9000/mcp", headers=None, auth=None
        )


if __name__ == "__main__":
    unittest.main()
