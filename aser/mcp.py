import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
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

        return self._run_async_in_sync(get_tools)

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

        tools = self._run_async_in_sync(get_tools)
        for tool in tools:
            if tool.name == tool_name:
                return tool
        return None

    def call_tool(self, tool_name, arguments):
        async def call_tool():
            async with self.client:
                result = await self.client.call_tool(tool_name, arguments)
                return result

        return self._run_async_in_sync(call_tool)

    def has_tool(self, tool_name):
        tools = self.get_tools()
        for tool in tools:
            if tool.name == tool_name:
                return True
        return False

    def _run_async_in_sync(self, async_func):
        """
        Generic method for running async functions synchronously
        Automatically handles event loop conflicts
        """
        def run_in_thread():
            return asyncio.run(async_func())

        try:
            # Try to get the currently running event loop
            asyncio.get_running_loop()
            # If already in an event loop, use thread pool to run
            with ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result()
        except RuntimeError:
            # If no running event loop, use asyncio.run directly
            return asyncio.run(async_func())
