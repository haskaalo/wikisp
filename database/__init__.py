import mysql.connector as database
import database.databasehelper as dh
import os


def connect():
    username = os.environ.get("DB_USER") or "root"
    password = os.environ.get("DB_PASSWORD") or ""
    host = os.environ.get("DB_HOST") or "localhost"
    if os.environ.get("DB_PORT") is None:
        port = 3306
    else:
        port = int(os.environ.get("DB_PORT"))

    dbname = os.environ.get("DB_DBNAME")

    try:
        connection = database.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database=dbname
        )

        cursor = connection.cursor()
        print("CONNECTED TO DATABASE!")
        return dh.DatabaseHelper(cursor, connection)
    except Exception as e:
        raise e
