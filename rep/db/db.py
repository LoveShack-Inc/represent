import sqlite3
import logging

class SqliteConnector:
    @classmethod
    def get_conn(self):
        return sqlite3.connect('./database/db.sqlite')

    def create_db(self):
        conn = SqliteConnector.get_conn()
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
                repVote VARCHAR NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
        logging.info("DB initialized")

    def run_migrations(self):
        conn = SqliteConnector.get_conn()
        c = conn.cursor()

        logging.info("Running migrations")
        c.executescript('''
        INSERT OR IGNORE INTO raw_vote_object_format (format) VALUES ('PDF');
        INSERT OR IGNORE INTO raw_vote_object_source_type (type) VALUES ('CT_STATE_GOV');
        ''')

        conn.commit()
        conn.close()
        logging.info("Done running migrations")
