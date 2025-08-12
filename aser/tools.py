class Tools:
    def __init__(self):
        self.tools = []
        self.functions = []

    def add(self, name, description, function, parameters,strict=False,extra_prompt=None):
        self.tools.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                    "strict": strict
                }
            }
        )
        self.functions.append({
            "name": name,
            "function":function,
            "extra_prompt":extra_prompt
        })
    
    def get_tool(self,tool_name):
        return [tool for tool in self.tools if tool["function"]["name"] == tool_name][0]
    
    def get_tools(self):
        return self.tools

    def get_function(self,function_name):
        return [tool for tool in self.functions if tool["name"] == function_name][0]


    def load_toolkits(self,toolkits):
        
        for toolkit in toolkits:
            for tool in toolkit:
                self.tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["parameters"],
                        "strict":tool["strict"]
                    }
                })
                self.functions.append({
                    "name": tool["name"],
                    "function":tool["function"],
                    "extra_prompt":tool["extra_prompt"]
                })
        


    
