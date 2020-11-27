import os 
import sqlite3

def sqlite_get_connection_helper():
    sqlite_db = os.getenv("SQLITE_FILEPATH", "./database/db.sqlite")
    if not os.path.isfile(sqlite_db):
        with open(sqlite_db, 'w') as f:
            pass
    return sqlite3.connect(sqlite_db, check_same_thread=False)
