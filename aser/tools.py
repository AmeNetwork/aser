from aser.utils import get_function_parameters


class Tools:
    def __init__(self, toolkits):
        self.tools = []
        self.functions = []
        self.load_toolkits(toolkits)

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

    def load_toolkits(self, toolkits):

        for toolkit in toolkits:
            if isinstance(toolkit, list):
                for tool in toolkit:
                    self.tools.append(
                        {
                            "type": "function",
                            "function": {
                                "name": tool["name"],
                                "description": tool["description"],
                                "parameters": tool["parameters"],
                            },
                        }
                    )
                    self.functions.append(
                        {"name": tool["name"], "function": tool["function"]}
                    )
            else:

                self.tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": toolkit["name"],
                            "description": toolkit["description"],
                            "parameters": toolkit["parameters"],
                        },
                    }
                )
                self.functions.append(
                    {"name": toolkit["name"], "function": toolkit["function"]}
                )

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
