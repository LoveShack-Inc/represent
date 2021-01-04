import sqlite3
import logging
from os import getenv
from rep.db import sqlite_get_connection_helper
import csv
from rep.dao.RepresentativeInfoDao import RepresentativeInfoDao

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
                repId INTEGER NOT NULL,
                repVote VARCHAR NOT NULL,
                rawVoteObjectId INTEGER NOT NULL,
                FOREIGN KEY (rawVoteObjectId) REFERENCES raw_vote_object(id),
                PRIMARY KEY (rawVoteObjectId, repId)
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

        filename = 'database/data/LegislatorDatabase_2020.csv'
        with open(filename) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for field in reader:
                representative_info_dao = RepresentativeInfoDao()
                # I can't get the auto-incrementing ID to work unless I give
                # a -1 as the first list entry for the dataclass.
                # I know this is bad!! But I don't know how else to fix it
                field.insert(0, -1)
                representative_info_dao.write(representative_info_dao._map_result(field))

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
