"""Free web search and page fetching through Aser's HTTP MCP client.

See parallel-search.md for installation and command examples.
"""

import argparse

from aser.mcp import MCP


def create_mcp():
    return MCP(
        "https://search.parallel.ai/mcp",
        header={"User-Agent": "aser-parallel-search-example/0.1.9"},
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    search = commands.add_parser("search", help="Search without a model or API key")
    search.add_argument("query")
    fetch = commands.add_parser("fetch", help="Fetch a page without a model or API key")
    fetch.add_argument("url")
    agent = commands.add_parser("agent", help="Let an Aser Agent choose an MCP tool")
    agent.add_argument("prompt")
    agent.add_argument("--model", default="gpt-4.1-mini")
    args = parser.parse_args()
    mcp = create_mcp()

    if args.command == "agent":
        from aser.agent import Agent

        agent = Agent(
            name="parallel search agent",
            description="Use web_search or web_fetch for current information. Cite source URLs.",
            model=args.model,
            mcp=[mcp],
        )
        print(agent.chat(args.prompt))
        return

    if args.command == "search":
        result = mcp.call_tool(
            "web_search",
            {"objective": args.query, "search_queries": [args.query]},
        )
    else:
        result = mcp.call_tool("web_fetch", {"urls": [args.url]})

    for content in result.content:
        if content.type == "text":
            print(content.text)


if __name__ == "__main__":
    main()
