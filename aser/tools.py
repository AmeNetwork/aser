from aser.utils import get_function_parameters


class Tools:
    def __init__(self, toolkits):
        self.tools = []
        self.functions = []
   

    def get_tool(self, tool_name):
        return [tool for tool in self.tools if tool["function"]["name"] == tool_name][0]

    def get_tools(self):
        return self.tools

    def get_function(self, function_name):
        return [tool for tool in self.functions if tool["name"] == function_name][0]

    def has_tool(self, tool_name):

        is_tool = False
        for tool in self.tools:
            if tool["function"]["name"] == tool_name:
                is_tool = True
                break
        return is_tool

    @staticmethod
    def tool(name=None, description=None):
        def decorator(func):
            parameters = get_function_parameters(func)
            return {
                "name": name or func.__name__,
                "description": description or func.__doc__,
                "parameters": parameters,
                "function": func,
            }

        return decorator


tool = Tools.tool
