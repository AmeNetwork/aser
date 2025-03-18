import string
import json
from eth_abi import encode, decode
from esper.mscp.connector import Connector
from esper.mscp.lib import solidity_to_openai_type

class Chat2Web3:
    def __init__(self,account):
        self.account=account
        self.methods = []
        self.functions = []
        self.account = account 
        
    def add(self, name, prompt, method):

        evm_component_method = {
            "name": name,
            "description": prompt,
            "method": method,
        }
        self.methods.append(evm_component_method)
        properties = {}
        for index in range(len(method["req"])):
            properties[string.ascii_letters[index]] = {}
            properties[string.ascii_letters[index]]["type"] = solidity_to_openai_type(
                method["req"][index]
            )
        function = {
            "type": "function",
            "function": {
                "name": name,
                "description": prompt,
                "parameters": {"type": "object", "properties": properties},
            },
        }
        self.functions.append(function)

    def call(self, function):
        method_data_values = list(json.loads(function.arguments).values())

        method = [item for item in self.methods if item["name"] == function.name][0]

        method_data_types = method["method"]["req"]

        encoded = "0x" + encode(method_data_types, method_data_values).hex()

        component = Connector(
            method["method"]["rpc"],
            method["method"]["address"],
        )
        method_response = component.send(
            type=method["method"]["type"],
            name=method["method"]["name"],
            params=encoded,
            value=0,
            account=self.account,
        )

        result = ""
        if method["method"]["type"] == "get":
            decoded = decode(method["method"]["res"], method_response)
            result = ",".join(map(str, decoded))
        else:
            result = "show tx hash to user" + "0x" + method_response

        return result


    def has(self,function_name):
        return any(item['name'] == function_name for item in self.methods)



        
