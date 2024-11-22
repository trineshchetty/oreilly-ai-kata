import streamlit as st
import os
from langchain_core.messages import AIMessage, HumanMessage
from langchain_aws import ChatBedrock
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# app config
st.set_page_config(page_title="Customer Service Bot", page_icon="🤖")
st.title("Customer Service Bot")


def get_database_connection():
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_host = os.environ.get("DB_ENDPOINT")
    db_port = 5432
    db_name = os.environ.get("DB_NAME")

    db_uri = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    try:
        # Use `from_uri` to initialize the SQLDatabase
        db = SQLDatabase.from_uri(db_uri)
        print("Database connection established successfully.")
        return db
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise


def normalize_query(query):
    # Remove comments
    lines = query.splitlines()
    stripped_lines = [line.split('--')[0].strip() for line in lines if not line.strip().startswith('--')]
    normalized_query = ' '.join(stripped_lines).strip()
    return normalized_query.lower()


def get_response(user_query, chat_history):
    db = get_database_connection()

    def run_query(query):

        normalized = normalize_query(query)

        if normalized.startswith('select'):
            return db.run(query)
        else:
            return "Invalid SQL query. Please provide a valid SELECT or SHOW statement."

    # SQL generation template
    sql_template = """
    Act as a Customer Service Representative.

    Based on the following schema, write a SQL query to answer the user's question. 
    If the user's question cannot be answered with a SQL query, respond with "No SQL query needed."
    Do not provide explanations, preambles, or additional text. Only output the SQL query or the exact phrase "No SQL query needed."

    Follow these rules strictly:
    - Do not include any descriptive text, comments, or markdown formatting.
    - Ensure the output begins directly with the SQL query or "No SQL query needed."
    - If the user asks about sales, for example top selling products, count the number of products ordered.
    - When filtering data, prioritize using `LIKE` or `tsvector` methods to search for keywords in the `name`, `description`, and `category` fields, especially if the user provides general terms or categories.
    - Ensure the SQL query retrieves relevant information even if exact matches are not found in the `category` column.

    Schema: {schema}
    Question: {question}
    """
    
    sql_prompt = ChatPromptTemplate.from_template(sql_template)

    # Response template
    response_template = """
    ShopWise Solutions is an innovative and fast-growing e-commerce company based in Austin,
    Texas, USA. Our online platform hosts a wide range of consumer products, spanning
    electronics, apparel, home goods, and much more. ShopWise Solutions has built a reputation
    for exceptional customer experience, streamlined order fulfillment, and a diverse catalog of
    quality products. We also deliver Globally.


    Conditions for conversations:
    1. If the user greets you, please greet back.
    2. If the user asks you about the business, do answer.
    3. If the user asks about anything else besides products, orders and Shopwise, ensure that they understand that you are only able to provice information on Shopwise Products and Orders.
    4. Do not sound technical.


    Based on the table schema below, question, sql query, and sql response, write a natural language response:
    Schema: {schema}
    
    If the SQL query does not return any data attempt to query the alternative table.
    For example if orders return no data, try querying the product table.

    Question: {question}
    SQL Query: {query}
    SQL Response: {response}

    Chat History: {chat_history}
    """
    
    response_prompt = ChatPromptTemplate.from_template(response_template)

    llm = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name=os.environ.get("AWS_REGION")
    )

    # Get schema once
    sql_schema = db.get_table_info()

    # SQL Generation Chain
    sql_chain = (
        RunnablePassthrough.assign(schema=lambda _: sql_schema)
        | sql_prompt
        | llm.bind(stop=["\SQL Query:"])
        | StrOutputParser()
    )

    def process_sql_response(vars):
        query = vars["query"]
        if query.strip().lower() == "no sql query needed":
            return "No SQL query was needed to answer this question."
        else:
            if "limit" not in query.lower():
                query = query.rstrip(";")
                query += " LIMIT 100"
            
            result = run_query(query)

            print(result)
            return result

    # Full chain
    full_chain = (
        RunnablePassthrough.assign(query=sql_chain)
        .assign(
            schema=lambda _: sql_schema,
            response=process_sql_response,
            chat_history=lambda _: chat_history
        )
        | response_prompt
        | llm
        | StrOutputParser()
    )

    return full_chain.stream({"question": user_query})

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, Welcome to Shopwise Solutions. My name is Elly, your AI Assistant. How may I help you today?"),
    ]

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))