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
        self.chat2web3 = properties.get("chat2web3", None)
        self.tools = properties.get("tools", [])
        self.__setup()

    def __setup(self):
        self.agent = OpenAI(
            base_url=os.getenv("OPENAI_API_BASE"),
            api_key=os.getenv("OPEN_AI_KEY"),
        )

        # self.agent = OpenAI(
        #     base_url=os.getenv("OPENAI_API_BASE"),
        #     api_key=os.getenv("OPEN_AI_KEY"),
        # )

       
        # set chat2web3
        if self.chat2web3:
            self.tools.extend(self.chat2web3.get_onchain().functions)

    def chat(self, text, uid=None):

        if uid is None:
            uid=self.name
               
        system_message = {"role": "system", "content": self.description}
        messages = [system_message]

        # set knowledge
        if self.knowledge:
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            knowledge_result = self.knowledge.query(text)
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

        user_message = {"role": "user", "content": text}

        # set memory
        if self.memory:
            history = self.memory.query(key=uid)
            if history:
                for item in history:
                    messages.append({"role": item["role"], "content": item["content"]})
            self.memory.insert(
                key=uid,
                role=user_message["role"],
                content=user_message["content"],
            )

        messages.append(user_message)

        response = self.agent.chat.completions.create(
            model=self.model, tools=self.tools, messages=messages
        )

        function_message = response.choices[0].message

        if function_message.tool_calls:

            function = function_message.tool_calls[0].function

            if self.chat2web3.is_onchain_tool_function(function.name):

                result = self.chat2web3.call(function)

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
                        key=uid,
                        role=return_message["role"],
                        content=return_message["content"],
                    )

                return return_message

        else:

            return_message = {"role": "assistant", "content": function_message.content}
            if self.memory:
                self.memory.insert(
                    key=uid,
                    role=return_message["role"],
                    content=return_message["content"],
                )
            return return_message
