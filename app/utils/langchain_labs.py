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
from app.utils.prompts import text2SQL_template, data_to_natural_language

model_chat = ChatOpenAI()


class SQLCommandOutputParser(BaseOutputParser):
    """Parse the output to SQL Query notation"""
    def parse(self, text: str) -> Any:
        global SQL_QUERY
        print(text)
        SQL_QUERY = text
        #QUERY_DICT = ast.literal_eval(text)
        print(type(SQL_QUERY))
        print(SQL_QUERY)
        return super().parse(text)


# Get templates
target_table_description_fields = get_target_table_description()

base_template = text2SQL_template(
    target_table=TARGET_TABLE,
    target_table_description_fields= target_table_description_fields
    )

human_template = "{text}"


# Load chatprompt
chat_prompt = ChatPromptTemplate.from_messages([
    ('system', base_template),
    ('human', human_template),
])


# LLM text2SQL
def transform2SQL(user_id, question: str):

    chain = chat_prompt | ChatOpenAI() | SQLCommandOutputParser()
    chain.invoke({"text": f"I am the user_id {user_id}. {question}"})

    try:
        
        generated_sql = SQL_QUERY
        
        # ************* TODO *************
        # Only validate SELECT (no clauses like WHERE) Find a better way ASAP.
        query_validated = sqlvalidator.parse(generated_sql)
        if not query_validated.is_valid():
            raise ValueError("Query Error", query_validated.errors)
        print("SQL PASS Validation.")
        print(generated_sql)
        return generated_sql
    except NameError as e:
        print("ERROR: ", e)


# ---
# AI RESPONSE TO THE USER

llm = OpenAI()

def data2Text_model(query: str, question: str, db_data_response: str):

    data_to_text_template = data_to_natural_language(user_question=question, db_query=query, data=db_data_response)    
    print("INTO GENERATE RESPONSE")
    print(data_to_text_template)
    print("***")

    for chunk in llm.stream(data_to_text_template):
        print(chunk, end="", flush=True)
