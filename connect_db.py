import psycopg
import dotenv
import os

dotenv.load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

with psycopg.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")