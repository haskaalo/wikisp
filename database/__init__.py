import database.databasehelper as dh
import sqlite3
import os


def connect():

    db = sqlite3.connect(os.environ.get("SQLITE3_DB_PATH") or "wikigraph.db")

    # Create tables if not exist
    print(os.getcwd())
    cursor = db.cursor()
    with open('./database/migrations/1_init_sqlite.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    db.commit()
    sql_file.close()

    try:
        return dh.DatabaseHelper(db)
    except Exception as e:
        raise e
