import psycopg2
import streamlit as st

def get_connection():
    """
    Establishes and returns a connection to the database.
    """
    try:
        connection = psycopg2.connect(
            database="xdfipckk",
            user="xdfipckk",
            password="3XIvuo-lGwvQ4swylHeaGzY1S4s1MDGI",
            host="ella.db.elephantsql.com",
            port="5432"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None
