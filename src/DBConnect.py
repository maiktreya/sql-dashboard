import psycopg2
import streamlit as st


def get_connection():
    """
    Establishes and returns a connection to the database.
    """
    try:
        connection = psycopg2.connect(
            database=st.secrets.postgresql["database"],
            user=st.secrets.postgresql["user"],
            password=st.secrets.postgresql["password"],
            host=st.secrets.postgresql["host"],
            port=st.secrets.postgresql["port"],
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None
