from openai import OpenAI
from dotenv import load_dotenv
from core.ame.ame_component import AmeComponent
import os
import string


from eth_account import Account
import json
load_dotenv()


class Esper:
    def __init__(self, **properties):
        self.name = properties["name"]
        self.model = properties["model"]
        self.description = properties["description"]
        self.memory = properties.get("memory", None)
        self.knowledge = properties.get("knowledge", None)
        self.chat2web3= properties.get("chat2web3",None)
        self.tools = properties.get("tools", [])

    def __setup():
        pass
        

    # def chat2web3(self, chat2web3_name, chat2web3_description, component_method):
    #     chat2web3 = {
    #         "name": chat2web3_name,
    #         "description": chat2web3_description,
    #         "component_method": component_method,
    #     }
    #     self.chat2web3s.append(chat2web3)

    #     properties = {}
    #     for index in range(len(component_method["req"])):
    #         properties[string.ascii_letters[index]] = {}
    #         properties[string.ascii_letters[index]]["type"] = (
    #             lib.solidity_to_openai_type(component_method["req"][index])
    #         )
    #     function = {
    #         "type": "function",
    #         "function": {
    #             "name": chat2web3_name,
    #             "description": chat2web3_description,
    #             "parameters": {"type": "object", "properties": properties},
    #         },
    #     }
    #     self.tools.append(function)

    def get_chat2web3s(self):
        return self.chat2web3s

    def get_chat2web3(self, chat2web3_name):
        for chat2web3 in self.chat2web3s:
            if chat2web3["name"] == chat2web3_name:
                return chat2web3
        return None

    def chat(self, question):

        self.agent = OpenAI(
            base_url=os.getenv("OPENAI_API_BASE"),
            api_key=os.getenv("OPEN_AI_KEY"),
        )

        system_message = {"role": "system", "content": self.description}
        messages = [system_message]

        # set knowledge
        if self.knowledge:
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            knowledge_result = self.knowledge.query(question)
            if len(knowledge_result["documents"][0]) > 0:
                knowledge_content = "\n".join(
                    f"{i+1}. {item}"
                    for i, item in enumerate(knowledge_result["documents"][0])
                )
                knowledge_message = {
                    "role": "assistant",
                    "content": knowledge_content,
                }
                messages.append(knowledge_message)

        user_message = {"role": "user", "content": question}

        # set memory
        if self.memory:
            history = self.memory.query(key=self.name)
            if history:
                for item in history:
                    messages.append({"role": item["role"], "content": item["content"]})
            self.memory.insert(
                key=self.name,
                role=user_message["role"],
                content=user_message["content"],
            )

        messages.append(user_message)

        # set chat2web3
        if self.chat2web3:
            self.tools.extend(self.chat2web3.get_onchain().functions)

        

        response = self.agent.chat.completions.create(
            model=self.model, tools=self.tools, messages=messages
        )

        function_message = response.choices[0].message

        if function_message.tool_calls:



            function = function_message.tool_calls[0].function

            if self.chat2web3.is_onchain_tool_function(function.name):
        
                result = self.chat2web3.call(function)

            # function_values = list(json.loads(function.arguments).values())
            # function_chat2web3 = [
            #     item for item in self.chat2web3s if item["name"] == function.name
            # ][0]
            # function_types = function_chat2web3["component_method"]["req"]

            # encoded = "0x" + encode(function_types, function_values).hex()

            # private_key = os.getenv("EVM_PRIVATE_KEY")
            # account = Account.from_key(private_key)
            # component = AmeComponent(
            #     function_chat2web3["component_method"]["rpc"],
            #     function_chat2web3["component_method"]["address"],
            # )
            # component_response = component.send(
            #     type=function_chat2web3["component_method"]["type"],
            #     name=function_chat2web3["component_method"]["name"],
            #     params=encoded,
            #     value=0,
            #     account=account,
            # )

            # result = ""
            # if function_chat2web3["component_method"]["type"] == "get":
            #     decoded = decode(
            #         function_chat2web3["component_method"]["res"], component_response
            #     )
            #     result = ",".join(map(str, decoded))
            # else:
            #     result = "show tx hash to user" + "0x" + component_response



                tool_message = {
                    "role": "tool",
                    "tool_call_id": function_message.tool_calls[0].id,
                    "content": result,
                }
                messages.append(function_message)
                messages.append(tool_message)

                tool_response = self.agent.chat.completions.create(
                    model=self.model, tools=self.tools, messages=messages
                )

                return_message = {
                    "role": "assistant",
                    "content": tool_response.choices[0].message.content,
                }

                if self.memory:
                    self.memory.insert(
                        key=self.name,
                        role=return_message["role"],
                        content=return_message["content"],
                    )

                return return_message

        else:

            return_message = {"role": "assistant", "content": function_message.content}
            if self.memory:
                self.memory.insert(
                    key=self.name,
                    role=return_message["role"],
                    content=return_message["content"],
                )
            return return_message
