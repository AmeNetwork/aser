# deed.page MCP

Use Aser's HTTP MCP client to publish HTML to a public `https://<slug>.deed.page/`
URL with the [deed.page](https://deed.page/docs) MCP server. Publishing needs no
account, API key or language model. Published pages are public.

Install Aser as described in [parallel-search.md](./parallel-search.md):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . -c examples/parallel-search-constraints.txt
```

Publish a sample page that expires after an hour, your own HTML file, or delete
a page you own:

```bash
python examples/agent_deed_page.py publish
python examples/agent_deed_page.py publish report.html --slug my-report-1234 --ttl 0
python examples/agent_deed_page.py delete my-report-1234
```

`--ttl 0` keeps the page. The first publish returns an owner token. The example
saves it to `~/.config/deed-page/token` (mode 600), or reads `DEEDPAGE_TOKEN`, and
passes it as `MCP(..., auth=token)` so later publishes and deletes stay under the
same owner. The token is never printed.

To let an Aser Agent publish its own output, pass a deed.page MCP instance to it:

```python
from aser.agent import Agent
from aser.mcp import MCP

deed_page = MCP("https://deed.page/mcp", header={"User-Agent": "my-aser-agent"})
agent = Agent(
    name="publisher",
    description="Write a short HTML page and publish it with publish_site. Reply with the URL.",
    model="gpt-4.1-mini",
    mcp=[deed_page],
)
```

The server exposes 26 tools (publishing, versions, domains and more). Agent mode
needs your model credentials (`MODEL_KEY`); see the main README.
