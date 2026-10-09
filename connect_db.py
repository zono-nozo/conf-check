import psycopg
import dotenv
import os

dotenv.load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

def connect_to_db():
    """
    Connects to the PostgreSQL database using credentials from environment variables.
    """
    return psycopg.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

def get_conferences_to_check(connection):
    """
    Retrieves the conference URLs and their corresponding IDs from the database.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT conference_id,url FROM conferences;")
        return cursor.fetchall()

def update_conference_info(connection, conference_id, location, start_date, end_date):
    """
    Updates the conference dates and location in the database.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE conferences SET location = %s, start_date = %s, end_date = %s WHERE conference_id = %s;",
            (location, start_date, end_date, conference_id)
        )