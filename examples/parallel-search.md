# Parallel Search MCP

Use Aser's HTTP MCP client for free web search and page fetching with
[Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp).
The anonymous endpoint needs no Parallel account or API key. Search uses Fast
mode; the free endpoint has rate limits.

From the repository root, use Python 3.13.2 or later and install Aser in a fresh
virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . -c examples/parallel-search-constraints.txt
```

The example's constraint selects the A2A SDK version compatible with Aser 0.1.9's
imports. No additional MCP dependency is needed.

Search and fetch directly, without configuring a language model:

```bash
python examples/agent_parallel_search.py search "Python asyncio TaskGroup documentation"
python examples/agent_parallel_search.py fetch https://docs.python.org/3/library/asyncio-task.html
```

To let an Aser Agent choose a tool, configure your model credentials as described
in the main README (`MODEL_KEY` and optionally `MODEL_BASE_URL`), then run:

```bash
python examples/agent_parallel_search.py agent "Search for Python TaskGroup documentation and cite a source URL."
```

Use `--model` after `agent` to select another model with tool calling support.
Aser's current `Agent.chat` handles one tool call followed by an answer; use the
direct commands above when you need to fetch a URL after searching.

The example uses `MCP(..., header={...})` and can also be adapted by passing the
returned MCP instance to your own `Agent(mcp=[...])`.
