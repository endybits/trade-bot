from fastapi import FastAPI

from app.config.config import get_openai_apikey

app = FastAPI()

OPENAI_APIKEY = get_openai_apikey()

@app.get('/')
def hello_trader():
    return {
        'msg': 'Hello Trader'
    }