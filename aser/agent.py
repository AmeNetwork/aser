from openai import OpenAI
from aser.utils import get_model_env, knowledge_to_prompt, chain_of_think
from aser.tools import Tools
import json
import time


class Agent:
    def __init__(self, **properties):

        self.name = properties["name"]
        self.avatar = properties.get("avatar", None)
        self.model = properties["model"]
        self.description = properties.get("description", "")
        self.memory = properties.get("memory", None)
        self.knowledge = properties.get("knowledge", None)
        self.tools_functions = []

        if properties.get("tools"):
            tools = Tools()
            tools.load_toolkits(properties.get("tools"))

            self.tools = tools

            self.tools_functions.extend(tools.get_tools())

        else:
            self.tools = None

        if properties.get("chat2web3"):
            self.chat2web3 = properties.get("chat2web3")
            self.tools_functions.extend(self.chat2web3.functions)

        else:
            self.chat2web3 = None

        if properties.get("mcp"):
            self.mcp = properties.get("mcp")
            for mcp in self.mcp:
                self.tools_functions.extend(mcp.get_tools_functions())
        else:
            self.mcp = None

        self.max_completion_tokens = properties.get("max_completion_tokens", None)
        self.max_token = properties.get("max_token", None)

        self.trace = properties.get("trace", None)
        self.error = None
        self.tools_log = None

        self.agent = OpenAI(**get_model_env(self.model))

    def get_info(self):
        return {
            "name": self.name,
            "avatar": self.avatar,
            "model": self.model,
            "description": self.description,
            "memory": self.memory,
            "knowledge": self.knowledge,
            "tools": self.tools,
            "chat2web3": self.chat2web3,
            "max_completion_tokens": self.max_completion_tokens,
            "max_token": self.max_token,
            "trace": self.trace,
        }

    def thinking(self, text):
        return chain_of_think(text, self.chat)

    def chat(self, text, uid=None, pre_messages=[], response_format=None):

        try:
            start_time = int(time.time() * 1000)
            system_message = {"role": "system", "content": self.description}
            messages = [system_message]

            # set knowledge
            if self.knowledge:

                knowledge_content = knowledge_to_prompt(self.knowledge, text)

                knowledge_message = {
                    "role": "assistant",
                    "content": knowledge_content,
                }
                messages.append(knowledge_message)

            # set pre_messages
            if pre_messages != []:
                messages.extend(pre_messages)

            user_message = {"role": "user", "content": text}

            # set memory
            if self.memory:
                history = self.memory.query(key=uid)
                if history:
                    for item in history:
                        messages.append(
                            {"role": item["role"], "content": item["content"]}
                        )
                self.memory.insert(
                    key=uid,
                    role=user_message["role"],
                    content=user_message["content"],
                )

            messages.append(user_message)

            params = {
                "model": self.model,
                "messages": messages,
                "max_completion_tokens": self.max_completion_tokens,
                "max_tokens": self.max_token,
            }

            if self.tools_functions:
                params["tools"] = self.tools_functions

            return_message = None

            if response_format:
                params["response_format"] = response_format
                completion = self.agent.chat.completions.parse(**params)

            else:
                completion = self.agent.chat.completions.create(**params)

            function_message = completion.choices[0].message

            if function_message.tool_calls:

                function = function_message.tool_calls[0].function

                self.tools_log = json.dumps(
                    {
                        "name": function.name,
                        "arguments": json.loads(function.arguments),
                    }
                )

                function_rsult = None

                # call chat2web3
                if self.chat2web3 != None and self.chat2web3.has(function.name):

                    function_rsult = self.chat2web3.call(function)

                # call mcp
                if self.mcp != None:

                    for mcp in self.mcp:
                        if mcp.has_tool(function.name):
                            function_rsult = mcp.call_tool(
                                function.name, json.loads(function.arguments)
                            ).content

                            break

                # call tools

                if self.tools != None and self.tools.has_tool(function.name):

                    toolkit_function = self.tools.get_function(function.name)

                    function_rsult = toolkit_function["function"](
                        **json.loads(function.arguments)
                    )

                    if toolkit_function["extra_prompt"]:
                        messages.append(
                            {
                                "role": "assistant",
                                "content": toolkit_function["extra_prompt"],
                            }
                        )

                tool_message = {
                    "role": "tool",
                    "tool_call_id": function_message.tool_calls[0].id,
                    "content": function_rsult,
                }
                messages.append(function_message)
                messages.append(tool_message)

                params["messages"] = messages

                tool_response = self.agent.chat.completions.create(**params)

                return_message = {
                    "role": "assistant",
                    "content": tool_response.choices[0].message.content,
                }

            else:

                return_message = {
                    "role": "assistant",
                    "content": function_message.content,
                }

            if self.memory:
                self.memory.insert(
                    key=uid,
                    role=return_message["role"],
                    content=return_message["content"],
                )

            return return_message["content"]
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            import traceback

            traceback.print_exc()
            self.error = str(e)
            return_message = {
                "role": "assistant",
                "content": "Sorry, I am not able to answer your question.",
            }
            return return_message["content"]
        finally:

            if self.trace:

                self.trace.add(
                    uid=uid,
                    session=self.trace.session,
                    agent_name=self.name,
                    agent_model=self.model,
                    input=text,
                    output=return_message["content"],
                    tools_log=self.tools_log,
                    start_time=start_time,
                    end_time=int(time.time() * 1000),
                    feed_back=None,
                    error=self.error,
                )
