from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_trader():
    return {
        'msg': 'Hello Trader'
    }