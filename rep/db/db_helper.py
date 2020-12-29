import sqlite3
import logging
from rep.db import sqlite_get_connection_helper
import csv
import os
from rep.dao.RepresentativeInfoDao import RepresentativeInfoDao

# Run this script to import the representatives into 
# the representative_info table

def representative_info():
    kwargs = {}
    conn = kwargs.get('database', sqlite_get_connection_helper())
    c = conn.cursor()

    logging.info("Initializing Representative Info table...")
    c.executescript('''

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
    conn.close()

    filename = 'database/data/LegislatorDatabase_2020.csv'
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for field in reader:
            representative_info_dao = RepresentativeInfoDao()
            representative_info_dao.write(representative_info_dao._map_result(field))

    logging.info("Representative Info table initialized")

representative_info()
