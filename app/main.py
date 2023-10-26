from pydantic import BaseModel, Field

from fastapi import FastAPI
from fastapi import status
from fastapi import Body


from app.utils.langchain_labs import transform2SQL, generateResponse
from app.utils.db_tests import db_querier

# Schema
class UserQuery(BaseModel):
    user_id: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="3"
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
    db_response_list_to_str = '\n'.join([''.join(str(col)) for col in db_response_list])
    print(db_response_list_to_str)


    # 1. data to image 2. Data to natural language
    
    # elaborate response
    generateResponse(
        query=sql_command,
        question=user_query.question,
        db_response=db_response_list_to_str
        )

    return {
        'user_query': user_query,
        'SQL': sql_command,
        'DB_resp': db_response_list
    }