import asyncio
from pydantic import BaseModel, Field

from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi.responses import StreamingResponse, JSONResponse

from app.utils.langchain_labs import transform2SQL, data2Text_model
from app.utils.db_tests import db_querier
from app.utils.chart_gpt import make_chart

# Schema
class UserQuery(BaseModel):
    user_id: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="4359"
    )
    question: str = Field(
        ...,
        min_length=8,
        example="which hour of the day is best to trade on tuesday in 2023? also show pnl grouped by other hours of the day"
    )



# API
app = FastAPI()

@app.get('/')
def hello_trader():
    return {
        'msg': 'Hello Trader'
    }


@app.post('/query-ai',
    status_code=status.HTTP_200_OK
)
def tradeInterpreterAI(
    user_query: UserQuery = Body(...)
):
    
    sql_command = transform2SQL(
        user_id=user_query.user_id,
        question=user_query.question
        )

    print(sql_command)
    # exec query agaist bd table
    db_response_list = db_querier(sql_command)
    data_str = '\n'.join([''.join(str(col)) for col in db_response_list])
    print(data_str)


    # 1. data to image 2. Data to natural language
    
    # elaborate response
    data2Text_model(
        query=sql_command,
        question=user_query.question,
        db_data_response=data_str
        )

    make_chart(
        user_question=user_query.question,
        sql_query=sql_command,
        db_data=data_str
    )

    return {
        'user_query': user_query,
        'SQL': sql_command,
        'DB_resp': db_response_list
    }



from fastapi.responses import Response, StreamingResponse
from typing import Any
import json
import orjson
class CustomJsonResponse(Response):
    media_type = "application/json"
    def render(self, content: Any):
        return orjson.dumps(content)
    



IM_NAME = "plot_20231030_214453.png"
IM_PATH = "/home/endyb/codev/trade-bot/data_plots/"
@app.get('/stream-answer', response_class=CustomJsonResponse)
async def get_custom_stream_answer():
    async def iter_file():
        await asyncio.sleep(2)
        resp = "AI answering: "
        for i in range(10000):
            resp += f"{i}"
            hi = {"user_idi": 123,
                    "question": "This is a fake question",
                    "value_i": i
                }
            yield orjson.dumps(hi)

    def text_background():
        for i in range(100000):
            # asyncio.sleep(2)
            print(i)
    response = {
        "user_id": 123,
        "question": "This is a fake question",
        #"answer": iter_file()
    }

    return StreamingResponse(content=iter_file(), media_type="application/json")