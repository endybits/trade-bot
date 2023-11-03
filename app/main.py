import asyncio
import json

from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import WebSocket, WebSocketException
from fastapi.responses import JSONResponse, HTMLResponse

from app.utils.langchain_labs import transform2SQL, data2Text_model
from app.utils.db_tests import db_querier
from app.utils.chart_gpt import make_chart
from app.utils.html_response import html


# Schema
class UserQuery(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=20, example="4359")
    question: str = Field(
        ...,
        min_length=8,
        example="which hour of the day is best to trade on tuesday in 2023? also show pnl grouped by other hours of the day",
    )


# API
app = FastAPI()


@app.get("/")
def hello_trader():
    return HTMLResponse(html)


@app.post("/query-ai", status_code=status.HTTP_200_OK)
def tradeInterpreterAI(user_query: UserQuery = Body(...)):
    sql_command = transform2SQL(
        user_id=user_query.user_id, question=user_query.question
    )

    print(sql_command)
    # exec query agaist bd table
    db_response_list = db_querier(sql_command)
    data_str = "\n".join(["".join(str(col)) for col in db_response_list])
    print(data_str)

    # 1. data to image 2. Data to natural language

    # elaborate response
    ai_response = data2Text_model(
        query=sql_command, question=user_query.question, db_data_response=data_str
    )

    chart_url = make_chart(
        user_question=user_query.question, sql_query=sql_command, db_data=data_str
    )
    response = {
        "user_question": user_query.question,
        "ai_answer": str(ai_response).strip(),
        "chart_url": chart_url,
    }
    return JSONResponse(response, media_type="application/json")


@app.websocket('/ws')
async def websocket_endpoint(
    websocket: WebSocket
):
    await websocket.accept()
    while True:
        #data = await websocket.receive_text()
        user_query = await websocket.receive_json(mode="text")
        question_obj = json.loads(user_query)
        question = question_obj.get("question")
        user_id = question_obj.get("user_id")
        await websocket.send_text(f"""{question}""")
        
        # GET SQL COMMAND
        sql_query = await transform2SQL(user_id, question)
        
        # exec query agaist bd table
        db_response_list = db_querier(sql_query)
        data_str = "\n".join(["".join(str(col)) for col in db_response_list])
        
        # Data to text
        ai_response = data2Text_model(
            query=sql_query, question=question, db_data_response=data_str
        )
        await websocket.send_text(f"""{ai_response}""")

        # Get Chart URL
        url = await make_chart(user_question=question, sql_query=sql_query, db_data=data_str)
        await websocket.send_text(f"""{url}""")