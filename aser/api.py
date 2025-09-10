from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import secrets


# class ChatRequest(BaseModel):
#     text: str
#     uid: str = None


class API:
    def __init__(self, agent, version="v1", allow_origins=["*"], verify=None):
        self.app = FastAPI()
        self.version = version
        self.agent = agent
        self.verify = verify
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.__setup_routes()

    def verify_key(self, request: Request):
        if self.verify == None:
            return True
        else:
            key = request.headers.get("key")
            uid = request.headers.get("uid")
            if self.verify(uid, key):
                return True
            else:
                raise HTTPException(status_code=401, detail="key verification failed")

    def __setup_routes(self):
        @self.app.get(f"/{self.version}/status")
        def get_status():
            return self.__response("success")

        @self.app.get(f"/{self.version}/agent", dependencies=[Depends(self.verify_key)])
        def get_agent():
            return self.__response("success", data=self.agent.get_info())

        @self.app.post(f"/{self.version}/chat", dependencies=[Depends(self.verify_key)])
        async def post_chat(request: Request):
            body =await request.json()
            text = body.get("text")
            uid = body.get("uid")
            result = self.agent.chat(text, uid)
            return self.__response("success", data=result)

    def __response(self, message, code=200, data=None):
        return {"code": code, "message": message, "data": data}

    def run(self, host="0.0.0.0", port=8000):
        uvicorn.run(self.app, host=host, port=port)

    def generate_key(self, uid):
        key = secrets.token_hex(32)
        return {"uid": uid, "key": key}
