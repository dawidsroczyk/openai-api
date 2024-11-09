import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text


# convert dataframe to database
def dataframe_to_database(df, table_name):

    engine = create_engine('sqlite:///:memory:', echo=True)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine


# handle response from openai api
def handle_response(response):

    query = ' '.join(response.choices[0].message.content.split('\n')[1:])
    return query


# execute query on an engine
def execute_query(engine, query):

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result