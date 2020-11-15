import logging

from rep.utils.logger import configure_logging
from rep.db.db import SqliteConnector

def main(): 
    """
        Handle startup functionality required by crawler, processor, and webserver
    """
    configure_logging()
    logging.info("Bootstrap: START")

    logging.info("Initializing database")
    _init_db()

    logging.info("Bootstrap: DONE")

def _init_db():
    sqliteConnector = SqliteConnector()
    sqliteConnector.create_db()
    sqliteConnector.run_migrations()

main()
