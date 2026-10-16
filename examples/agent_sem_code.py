"""Query a trusted local Sem HTTP MCP endpoint without a language-model key.

See sem-code.md. Requires the Sem HTTP preview, not the 0.27.0 release.
"""
import argparse
import os

from aser.mcp import MCP


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Exact entity name, e.g. parse_config")
    args = parser.parse_args()
    token = os.environ.get("SEM_MCP_HTTP_TOKEN")
    if not token:
        parser.error("Set SEM_MCP_HTTP_TOKEN to the token used by your local Sem server")
    # Fixed loopback address: never forward this secret to a user-supplied URL.
    client = MCP("http://127.0.0.1:8765/mcp", header={"Authorization": f"Bearer {token}"})
    if not client.has_tool("sem_find"):
        raise RuntimeError("The endpoint does not advertise sem_find")
    result = client.call_tool("sem_find", {"query": args.query, "mode": "context", "token_budget": 1200})
    if result.is_error:
        raise RuntimeError("Sem returned a tool error; check the entity name and server checkout")
    for content in result.content:
        if content.type == "text":
            print(content.text)


if __name__ == "__main__":
    main()
