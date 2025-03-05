class Tools:
    def __init__(self):
        self.tools = []
        self.functions = []

    def add(self, name, description, function, parameters):
        self.tools.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters
                }
            }
        )
        self.functions.append({
            "name": name,
            "function":function
        })
    
    def get_tool(self,tool_name):
        return [tool for tool in self.tools if tool["function"]["name"] == tool_name][0]
    
    def get_tools(self):
        return self.tools

    def get_function(self,function_name):
        return [tool for tool in self.functions if tool["name"] == function_name][0]


    


    
