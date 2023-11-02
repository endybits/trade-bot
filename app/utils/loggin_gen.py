import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="tradeai_query.log",
)
logging.info(
    """user 1 - question: this is a question | SQL: SELECT * FROM fake_table | AI_observation: This is the AI Opinion about the query"""
)
