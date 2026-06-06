import psycopg2

""" Connects to the PostgreSQL database and returns the connection object """
def db_connection():
    conn = psycopg2.connect(
        host="database",
        database="watchflix_db", 
        user="postgres",
        password="123" 
    )
    return conn
        