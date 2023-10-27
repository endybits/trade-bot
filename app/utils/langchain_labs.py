import os
import ast
from typing import Any

from app.config.fconfig import get_openai_apikey as API_KEY
os.environ["OPENAI_API_KEY"] = API_KEY()

import sqlvalidator

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI

from app.utils.table_description import get_target_table_description
from app.utils.db_utils import TARGET_TABLE


model_chat = ChatOpenAI()


class SQLCommandOutputParser(BaseOutputParser):
    """Parse the output to SQL Query notation"""
    def parse(self, text: str) -> Any:
        global QUERY_DICT
        QUERY_DICT = ast.literal_eval(text)
        
        print(type(QUERY_DICT))
        print(QUERY_DICT)
        return super().parse(text)





# Pre-load templates
target_table_description_fields = get_target_table_description()
base_template = f"""You are a SQL expert assistant who generates SQL Query commands based on text.
                    A user will pass in a question and you should convert it in a SQL command 
                    to query against the table {TARGET_TABLE} in a MariaDB database.
                    Use this fields description of the table, for a more accurate results: {target_table_description_fields}
                    ONLY return a SQL Query, and nothing more."""

base_template = f"""You are a SQL expert assistant who generates SQL Query commands based on text.
                    A user will pass in a question and you should convert it in a SQL command 
                    to query against the table {TARGET_TABLE} in a MariaDB database.
                    Use this fields description of the table, for a more accurate results: {target_table_description_fields}
                    ONLY Python Dict with this structure: "sql_query: SELECT..., column_list: [field1, field2, ...]"."""

base_template.format(target_table_description_fields=target_table_description_fields, TARGET_TABLE=TARGET_TABLE)
human_template = "{text}"

# Pre-load chatprompt
chat_prompt = ChatPromptTemplate.from_messages([
    ('system', base_template),
    ('human', human_template),
])


def transform2SQL(user_id, question: str):

    chain = chat_prompt | ChatOpenAI() | SQLCommandOutputParser()
    chain.invoke({"text": f"I am the user_id {user_id}. {question}"})

    try:
        
        SQL_QUERY = QUERY_DICT['sql_query']
        query_validated = sqlvalidator.parse(SQL_QUERY) # Only validate SELECT (no clauses like WHERE) Find a better way ASAP.
        if not query_validated.is_valid():
            raise ValueError("Query Error", query_validated.errors)
        print("SQL PASS Validation.")
        print(SQL_QUERY)
        return SQL_QUERY
    except NameError as e:
        print("ERROR: ", e)



# ---
# AI RESPONSE TO THE USER

llm = OpenAI()

class AIAnswerOutputParser(BaseOutputParser):
    """Parse the output to User response"""
    def parse(self, text: str) -> Any:
        global NL_RESPONSE
        NL_RESPONSE = text
        return super().parse(text)
    

response_base_template = """You are a Trading expert assistant with a wide experience
                            helping users to understand their historical data.
                            Based on this user question: {USER_QUESTION} this DB query was generated: {DB_QUERY};
                            and subsequently executed against the database table {TARGET_TABLE} <<you can extract the description for each field here: {target_table_description_fields}>>. 
                            The resulting data is: {DATA}.
                            Your task is to interpret the resulting data from de DB and answer for the user.
                            Do not make information up."""



# human_template = "{text}"
def generateResponse(query: str, question: str, db_response: str):

    USER_QUESTION=question,
    DB_QUERY=query,
    DATA="10, 1695.0"

    response_base_template2 = f"""You are a Trading expert assistant with a wide experience
                            helping users to understand their historical data.
                            Using this sql query {DB_QUERY} was generated this data {DATA}. 
                            Based on it, Your task is answer this question {USER_QUESTION}.
                            Do not make information up, only write the answer and nothing more."""

    response_base_template.format(
        USER_QUESTION=question,
        DB_QUERY=query,
        TARGET_TABLE=TARGET_TABLE,
        target_table_description_fields=target_table_description_fields,
        #DATA=db_response
        DATA=db_response
        )
    
    # response_base_template2.format(
    #     USER_QUESTION=question,
    #     DB_QUERY=query,
    #     DATA="10, 1695.0"
    #     )
    
    # chain = LLMChain(llm=model, prompt=response_base_template2)
    # chain.run(USER_QUESTION=question, DB_QUERY=query)
    #chain.run(topic='trading')
    
    print("INTO GENERATE RESPONSE")
    print(response_base_template2)
    print("***")
    
    # llm.invoke(response_base_template)
    for chunk in llm.stream(response_base_template2):
        print(chunk, end="", flush=True)

    