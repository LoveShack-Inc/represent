import sqlite3
import logging
from os import getenv
from rep.db import sqlite_get_connection_helper

class SqliteConnector:
    def __init__(self, **kwargs):
        if 'database' not in kwargs:
            logging.warning("No database supplied, using default connection")
        self.conn = kwargs.get('database', sqlite_get_connection_helper())
    
    def create_db(self):
        conn = self.conn 
        c = conn.cursor()

        logging.info("Initializg DB")
        c.executescript('''
        CREATE TABLE IF NOT EXISTS raw_vote_object_format
            (
                id INTEGER NOT NULL PRIMARY KEY,
                format VARCHAR NOT NULL UNIQUE
            );

        CREATE TABLE IF NOT EXISTS raw_vote_object_source_type
            (
                id INTEGER NOT NULL PRIMARY KEY,
                type VARCHAR NOT NULL UNIQUE
            );

        CREATE TABLE IF NOT EXISTS raw_vote_object
            (
                id INTEGER NOT NULL PRIMARY KEY,
                blob BLOB NOT NULL, 
                sourceUrl VARCHAR NOT NULL UNIQUE,
                sourceType VARCHAR NOT NULL,
                format VARCHAR NOT NULL,
                isProcessed BOOLEAN NOT NULL DEFAULT FALSE,
                FOREIGN KEY (sourceType) REFERENCES raw_vote_object_source_type(type), 
                FOREIGN KEY (format) REFERENCES raw_vote_object_format(format)
            );
            
        CREATE TABLE IF NOT EXISTS processed_vote_result
            (
                unixTime INTEGER NOT NULL,
                billNumber VARCHAR NOT NULL,
                voteName VARCHAR NOT NULL,
                repName VARCHAR NOT NULL,
                repVote VARCHAR NOT NULL,
                rawVoteObjectId INTEGER NOT NULL,
                FOREIGN KEY (rawVoteObjectId) REFERENCES raw_vote_object(id),
                PRIMARY KEY (rawVoteObjectId, repName)
            );
        CREATE TABLE IF NOT EXISTS representative_info
            (
                id INTEGER NOT NULL PRIMARY KEY,
                firstName VARCHAR NULL,
                middleName VARCHAR NULL,
                lastName VARCHAR NOT NULL,
                state VARCHAR NOT NULL,
                party VARCHAR NULL
            );
        ''')

        conn.commit()
        logging.info("DB initialized")

    def run_migrations(self):
        conn = self.conn
        c = conn.cursor()

        logging.info("Running migrations")
        c.executescript('''
        INSERT OR IGNORE INTO raw_vote_object_format (format) VALUES ('PDF');
        INSERT OR IGNORE INTO raw_vote_object_source_type (type) VALUES ('CT_STATE_GOV');
        ''')

        conn.commit()
        logging.info("Done running migrations")
