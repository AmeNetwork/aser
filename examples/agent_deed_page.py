"""Publish HTML pages to public URLs through Aser's HTTP MCP client.

See deed-page.md for installation and command examples.
"""

import argparse
import json
import os
from pathlib import Path

from fastmcp.exceptions import ToolError

from aser.mcp import MCP

TOKEN_FILE = Path.home() / ".config" / "deed-page" / "token"
SAMPLE_PAGE = (
    "<!doctype html><html><head><meta charset='utf-8'><title>Aser</title></head>"
    "<body><h1>Published by an Aser agent</h1></body></html>"
)


def load_token():
    token = os.environ.get("DEEDPAGE_TOKEN", "").strip()
    if not token and TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text().strip()
    return token or None


def save_token(token):
    TOKEN_FILE.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    TOKEN_FILE.touch(mode=0o600, exist_ok=True)
    TOKEN_FILE.write_text(token)
    TOKEN_FILE.chmod(0o600)


def create_mcp(token=None):
    # The owner token, when present, is sent as an Authorization: Bearer header.
    return MCP(
        "https://deed.page/mcp",
        auth=token,
        header={"User-Agent": "aser-deed-page-example/0.1.9"},
    )


def call(mcp, args):
    if args.command == "publish":
        html = Path(args.file).read_text(encoding="utf-8") if args.file else SAMPLE_PAGE
        arguments = {"files": {"index.html": html}}
        if args.slug:
            arguments["slug"] = args.slug
        if args.ttl > 0:
            arguments["ttl_seconds"] = args.ttl
        return mcp.call_tool("publish_site", arguments)
    return mcp.call_tool("delete_site", {"slug": args.slug})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    publish = commands.add_parser(
        "publish", help="Publish an HTML file or a sample page"
    )
    publish.add_argument("file", nargs="?")
    publish.add_argument("--slug", help="Subdomain to claim; random when omitted")
    publish.add_argument(
        "--ttl", type=int, default=3600, help="Expiry in seconds; 0 keeps the page"
    )
    delete = commands.add_parser("delete", help="Delete a page you own")
    delete.add_argument("slug")
    args = parser.parse_args()

    token = load_token()
    if args.command == "delete" and not token:
        parser.error(
            "delete needs the owner token (DEEDPAGE_TOKEN or ~/.config/deed-page/token)"
        )
    mcp = create_mcp(token)

    try:
        result = call(mcp, args)
    except ToolError as error:
        raise SystemExit(f"deed.page error: {error}")

    text = "".join(c.text for c in result.content if c.type == "text")
    data = json.loads(text)
    if not data.get("ok"):
        raise SystemExit(f"deed.page error: {text}")
    if data.get("token"):
        save_token(data.pop("token"))
        print(f"Owner token saved to {TOKEN_FILE}")
    keys = (
        ("url", "slug", "version", "expires_at")
        if args.command == "publish"
        else ("ok",)
    )
    print(json.dumps({k: data[k] for k in keys if k in data}, indent=2))


if __name__ == "__main__":
    main()
