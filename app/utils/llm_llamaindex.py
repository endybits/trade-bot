import os
from sqlalchemy import create_engine, MetaData
from llama_index import LLMPredictor, ServiceContext, SQLDatabase, VectorStoreIndex
from llama_index.indices.struct_store import SQLTableRetrieverQueryEngine
from llama_index.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema

from langchain.llms.openai import OpenAI

from db_utils import MARIADB_URI, TARGET_TABLE

os.getenv("OPENAI_API_KEY")

engine = create_engine(MARIADB_URI)

# load all table definitions
meta_obj = MetaData()
meta_obj.reflect(engine)

sql_database = SQLDatabase(engine)

table_node_mapping = SQLTableNodeMapping(sql_database)

table_schema_objs = []
table_name_list = []
for table_name in meta_obj.tables.keys():
    table_name_list.append(table_name)
    table_schema_objs.append(SQLTableSchema(table_name=table_name))


# Dump the tale schemas into  a vector index.
obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)


## LLM
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model="gpt-3.5-turbo"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

# Query Engine
query_engine = SQLTableRetrieverQueryEngine(
    sql_database,
    obj_index.as_retriever(similarity_top_k=1),
    service_context=service_context,
)


response = query_engine.query(f"How many rows there are in the table {TARGET_TABLE}?")

print(response)
print(10 * "*")
print(response.metadata["sql_query"])
print(10 * "*")
print(response.metadata["result"])
