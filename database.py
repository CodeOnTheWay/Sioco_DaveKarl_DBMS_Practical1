import os
import pyodbc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "UserSystem.accdb")

CONNECTION_STRING = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    rf"DBQ={DB_PATH};"
)

def get_connection():
    return pyodbc.connect(CONNECTION_STRING)

def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Users")
        count = cursor.fetchone()[0]

        print("Database connected successfully!")
        print("Users table records:", count)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Database connection failed:")
        print(e)

if __name__ == "__main__":
    test_connection()