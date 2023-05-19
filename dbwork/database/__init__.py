import database.databasehelper as dh
import sqlite3
import os


def connect():

    db = sqlite3.connect(os.environ.get("SQLITE3_DB_PATH") or "wikigraph.db")

    try:
        return dh.DatabaseHelper(db)
    except Exception as e:
        raise e
