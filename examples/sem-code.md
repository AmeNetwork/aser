# Local code lookup with Sem over HTTP (preview)

This optional example exercises Aser's existing HTTP MCP client against a
self-hosted code server, rather than a web-search API. It discovers `sem_find`
and asks for an entity's source and related code. No model/API-provider key is
needed; a local server bearer token is required.

**Prerequisite:** the Sem Streamable HTTP preview source build. The published
Sem 0.27.0 release does not support this transport. Follow the source build and
startup instructions in [Sem's HTTP guide](https://github.com/Ataraxy-Labs/sem/blob/2e6a47fcd35ce269eec702dd3532341dba52902b/docs/mcp-http.md).
The transport landed in [Sem PR #518](https://github.com/Ataraxy-Labs/sem/pull/518).
Build Sem commit `2e6a47fcd35ce269eec702dd3532341dba52902b` or a later compatible version.
Start it on `127.0.0.1:8765` with `SEM_REPO` explicitly set to a trusted Git
checkout and `SEM_MCP_HTTP_TOKEN` set to a random secret. Run the client on the
same host. This is not a hosted service, and localhost is not your laptop when
the client runs in a cloud environment.

Install Aser as in the [Parallel example](parallel-search.md), then run from
the repository root, with the same token available in this terminal:

```sh
python examples/agent_sem_code.py parse_config
```

Replace `parse_config` with an entity that exists in your checkout. The script
uses `MCP(..., header={"Authorization": ...})`, checks tool discovery, calls
`sem_find`, and prints the text blocks. It never asks a model to choose a tool
and does not change Aser's defaults.

The server exposes discovery/read tools only; it does not expose editing,
builds, shell commands, or Weave merges. It can write its index/cache. Treat
anyone with the token as trusted to read the checkout; keep secrets out of the
repository and do not expose this preview to the internet. Stop the server
and remove the token when done. Do not commit tokens or `.env` files.
