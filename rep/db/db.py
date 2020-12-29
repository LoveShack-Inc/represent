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

        logging.info("Initializing DB")
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
                id INTEGER PRIMARY KEY,
                dist VARCHAR NULL,
                officeCode VARCHAR NULL,
                districtNumber VARCHAR NULL,
                designatorCode VARCHAR NULL,
                firstName VARCHAR NULL,
                middleInitial VARCHAR NULL,
                lastName VARCHAR NULL,
                suffix VARCHAR NULL,
                commonlyUsedName VARCHAR NULL,
                homeStreetAddress VARCHAR NULL,
                homeCity VARCHAR NULL,
                homeState VARCHAR NULL,
                homeZipCode VARCHAR NULL,
                homePhone VARCHAR NULL,
                capitolStreetAddress VARCHAR NULL,
                capitolCity VARCHAR NULL,
                capitolPhone VARCHAR NULL,
                room VARCHAR NULL,
                roomNumber VARCHAR NULL,
                committeesChaired VARCHAR NULL,
                committeesViceChaired VARCHAR NULL,
                rankingMember VARCHAR NULL,
                committeeMember1 VARCHAR NULL,
                senatorRepresentative VARCHAR NULL,
                party VARCHAR NULL,
                title VARCHAR NULL,
                gender VARCHAR NULL,
                businessPhone VARCHAR NULL,
                email VARCHAR NULL,
                fax VARCHAR NULL,
                prison VARCHAR NULL,
                url VARCHAR NULL,
                committeeCodes VARCHAR NULL
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
