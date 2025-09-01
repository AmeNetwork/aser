import asyncio
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.client import Client

class MCP:
    def __init__(self, url, auth=None, header=None):
        transport = StreamableHttpTransport(url, auth, header)
        client = Client(transport)

        async def get_client():
            async with client:
                return client

        self.client = asyncio.run(get_client())

    def get_tools(self):
        async def get_tools():
            async with self.client:
                tools = await self.client.list_tools()
                return tools

        return asyncio.run(get_tools())

    def get_tools_functions(self):
        tools = self.get_tools()
        functions = []
        for tool in tools:
            function = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": tool.inputSchema["properties"],
                    },
                    "required": (
                        tool.inputSchema["required"]
                        if "required" in tool.inputSchema
                        else None
                    ),
                },
            }
            functions.append(function)
        return functions

    def get_tool(self, tool_name):
        async def get_tools():
            async with self.client:
                tools = await self.client.list_tools()
                return tools

        tools = asyncio.run(get_tools())
        for tool in tools:
            if tool.name == tool_name:
                return tool
        return None

    def call_tool(self, tool_name, arguments):
        async def call_tool():
            async with self.client:
                result = await self.client.call_tool(tool_name, arguments)
                return result

        return asyncio.run(call_tool())

    def has_tool(self, tool_name):
        tools = self.get_tools()
        for tool in tools:
            if tool.name == tool_name:
                return True
        return False



