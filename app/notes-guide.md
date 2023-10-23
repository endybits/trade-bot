# Proposed service methodology

## User query interpretation
- Use a language understanding (LU) model to interpret the user's query and identify the relevant entities, intents, and slots.

## Query translation
- Translate the user's query into a SQL query that can be executed against the MariaDB database.

## Query execution
- Execute the SQL query against the MariaDB database and retrieve the requested data.

## Response generation
- Use a language generation (LG) model to generate a natural language response that is tailored to the user's query.

# Python-based LLM frameworks

## LangChain
- LangChain is a natural language processing (NLP) pipeline that can be used to chain together different NLP tasks, such as LU, query translation, and LG.

## LLAMAindex
- LLAMAindex is a search engine that can be used to retrieve relevant information from a corpus of text.

# Proposed service implementation

- Use LangChain to create an NLP pipeline that can interpret user queries, translate them into SQL queries, and generate natural language responses.
- Use LLAMAindex to index the MariaDB database so that relevant information can be retrieved quickly and efficiently.
- Deploy the NLP pipeline and LLAMAindex as a web service.

# Benefits of this approach

- This approach is flexible and can be adapted to a wide range of use cases.
- The use of LLM frameworks allows the service to be easily maintained and updated.
- The service can be deployed as a web service, making it accessible to a wide range of users.
