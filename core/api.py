from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def read_root():
    return {'Hello': 'World3'}


uvicorn.run(app, host="0.0.0.0", port=8000)