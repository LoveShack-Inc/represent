import sqlite3
import logging
from rep.db import sqlite_get_connection_helper
import csv
import os
import pandas as pd

# Run this script to import the representatives into 
# the representative_info table


kwargs = {}
conn = kwargs.get('database', sqlite_get_connection_helper())

c = conn.cursor()

logging.info("Initializg Representative Info table...")
c.executescript('''

        CREATE TABLE IF NOT EXISTS representative_info
            (
                id INTEGER NOT NULL PRIMARY KEY,
                dist VARCHAR NULL,
                officeCode VARCHAR NULL,
                districtNumber VARCHAR NULL,
                number VARCHAR NULL,
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

df = pd.read_csv('database/data/LegislatorDatabase_2020.csv')
df.to_sql('representative_info', conn, if_exists='append', index=False)

conn.commit()
conn.close()
logging.info("Representative Info table initialized")