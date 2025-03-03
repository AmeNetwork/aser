from fastapi import FastAPI, Body
import uvicorn


class API:
    def __init__(self, agent, version="v1"):
        self.app = FastAPI()
        self.version = version
        self.agent = agent
        self.__setup_routes()

    def __setup_routes(self):
        @self.app.get(f"/{self.version}/agent")
        def get_agent():
            return self.__response("success", self.agent.get_info())

        @self.app.post(f"/{self.version}/chat")
        def post_chat(text, uid=None):
            result = self.agent.chat(text, uid)
            return self.__response("success", data=result)

    def __response(self, message, code=200, data=None):
        return {"code": code, "message": message, "data": data}

    def run(self, host="0.0.0.0", port=8000):
        uvicorn.run(self.app, host=host, port=port)
