class Tools:
    def __init__(self):
        self.tools = []
        self.functions = []

    def create(self, name, description, function, parameters,extra_prompt=None,example=None):
        return [{
            "name": name,
            "description": description, 
            "parameters": parameters,
            "function": function,
            "extra_prompt": extra_prompt,
            "example":example
        }]


    def get_tool(self,tool_name):
        return [tool for tool in self.tools if tool["function"]["name"] == tool_name][0]
    
    def get_tools(self):
        return self.tools

    def get_function(self,function_name):
        return [tool for tool in self.functions if tool["name"] == function_name][0]

    def has_tool(self,tool_name):

        is_tool=False
        for tool in self.tools:
            if tool["function"]["name"] == tool_name:
                is_tool=True
                break
        return is_tool

    def load_toolkits(self,toolkits):

        for toolkit in toolkits:
                for tool in toolkit:
                    self.tools.append({
                        "type": "function",
                        "function": {
                            "name": tool["name"],
                            "description": tool["description"],
                            "parameters": tool["parameters"],
                        }
                    })
                    self.functions.append({
                        "name": tool["name"],
                        "function":tool["function"],
                        "extra_prompt":tool["extra_prompt"]
                    })
        
   
    
    
        


    
