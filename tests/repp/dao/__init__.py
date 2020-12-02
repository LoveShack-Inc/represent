# create an inmemory sqlite db for tests
import sqlite3

from rep.db.db import SqliteConnector 

inmemory_test_db = sqlite3.connect(":memory:")

def _seed_db(db):
    sqliteConnector = SqliteConnector(
        database=db
    )
    sqliteConnector.create_db()
    sqliteConnector.run_migrations()

def get_test_dao(dao, truncate_database):
    return_db = inmemory_test_db
    if truncate_database:
        return_db = sqlite3.connect(":memory:")
        _seed_db(return_db)

    return dao(database=return_db)

_seed_db(inmemory_test_db)
