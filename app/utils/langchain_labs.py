import os
from typing import Any

from app.config.fconfig import get_openai_apikey as API_KEY
os.environ["OPENAI_API_KEY"] = API_KEY()

import sqlvalidator

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

from app.utils.table_description import get_target_table_description
from app.utils.db_utils import TARGET_TABLE

class SQLCommandOutputParser(BaseOutputParser):
    """Parse the output to SQL Query notation"""
    def parse(self, text: str) -> Any:
        global SQL_QUERY
        SQL_QUERY = text
        return super().parse(text)


# Pre-load templates
table_structure = get_target_table_description()
base_template = f"""You are a SQL expert assistant who generates SQL Query commands based on text.
                    A user will pass in a question and you should convert it in a SQL command 
                    to query against the table {TARGET_TABLE} in a MariaDB database.
                    Use this field description of the table, for a more accurate results: {table_structure}
                    ONLY return a SQL Query, and nothing more."""

base_template.format(table_structure=table_structure, TARGET_TABLE=TARGET_TABLE)
human_template = "{text}"

# Pre-load chatprompt
chat_prompt = ChatPromptTemplate.from_messages([
    ('system', base_template),
    ('human', human_template),
])


Q = [
    "on which symbols did I pay the most commissions and fees?",
    "which hour of the day is best to trade on tuesday",
    "Trades with highest pnl on fridays show symbol, trade time, pnl",
    "total pnl of trades with r value lower than 2",
    "WITH the most recent 50 trades by open date from trading accounts Account 1 or Account 2 CALCULATE winning percentage",
    "which hour of the day is best to trade on tuesday in 2023? also show pnl grouped by other hours of the day",
]

def transform2SQL(user_id, question: str):

    chain = chat_prompt | ChatOpenAI() | SQLCommandOutputParser()
    chain.invoke({"text": f"I am the user_id {user_id}. {question}"})

    try:
        query_validated = sqlvalidator.parse(SQL_QUERY) # Only validate SELECT (no clauses like WHERE) Find a better way ASAP.
        if not query_validated.is_valid():
            raise ValueError("Query Error", query_validated.errors)
        print("SQL PASS Validation.")
        print(SQL_QUERY)
        return SQL_QUERY
    except NameError as e:
        print("ERROR: ", e)