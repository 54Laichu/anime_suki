import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager

load_dotenv()

DATABASE_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=3,
    **DATABASE_CONFIG
)

@contextmanager
def get_db():
    connection = connection_pool.get_connection()
    try:
        yield connection
    finally:
        connection.close()
