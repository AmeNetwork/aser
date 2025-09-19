import json


def handle_tool_function(function, chat2web3, mcp, tools):
    function_rsult = None
    if chat2web3 != None and chat2web3.has(function.name):
        function_rsult = chat2web3.call(function)

    if mcp != None:
        for mcp_item in mcp:
            if mcp_item.has_tool(function.name):
                function_rsult = mcp_item.call_tool(
                    function.name, json.loads(function.arguments)
                ).content
                break

    if tools != None and tools.has_tool(function.name):

        toolkit_function = tools.get_function(function.name)

        function_rsult = toolkit_function["function"](**json.loads(function.arguments))

    return function_rsult
    
