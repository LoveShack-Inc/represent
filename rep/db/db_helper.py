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

    # df = pd.read_csv('database/data/LegislatorDatabase_2020.csv')
    # df.to_sql('representative_info', conn, if_exists='append', index=False)
    filename = 'database/data/LegislatorDatabase_2020.csv'
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for field in reader:
            c.execute("INSERT INTO representative_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", field)

    conn.commit()
    conn.close()
    logging.info("Representative Info table initialized")

def bill_info():
    kwargs = {}
    conn = kwargs.get('database', sqlite_get_connection_helper())

    c = conn.cursor()

    logging.info("Initializg Bill Info table...")
    c.executescript('''

            CREATE TABLE IF NOT EXISTS bill_info
                (
                    id INTEGER NOT NULL PRIMARY KEY,
                    billNum VARCHAR NOT NULL,
                    lcoNum INTEGER NOT NULL,
                    sessYear INTEGER NOT NULL,
                    sessNum INTEGER NOT NULL,
                    typeCode VARCHAR NOT NULL,
                    billTitle VARCHAR NOT NULL,
                    stmtPurp VARCHAR NULL,
                    emergencyCert BOOLEAN NOT NULL,
                    raised BOOLEAN NOT NULL,
                    proposed BOOLEAN NOT NULL,
                    subBill BOOLEAN NOT NULL,
                    nomination BOOLEAN NOT NULL,
                    numPages INTEGER NOT NULL,
                    houseCalNum VARCHAR NULL,
                    senateCalNum VARCHAR NULL,
                    filedDate VARCHAR NOT NULL,
                    readIntoFloor VARCHAR NOT NULL,
                    petitionNum VARCHAR NULL,
                    pasaNum INTEGER NULL,
                    pasaType VARCHAR NULL,
                    senateAmd VARCHAR NULL,
                    houseAmd VARCHAR NULL
                );

    ''')

    # https://www.cga.ct.gov/ftp/pub/data/bill_info.csv
    df = pd.read_csv('database/data/bill_info_2020.csv')
    df.to_sql('bill_info', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    logging.info("Bill Info table initialized")

representative_info()
bill_info()
