import logging
from dataclasses import dataclass
from rep.dao.BaseDao import BaseDao
from rep.dataclasses.VoteObject import VoteObject

class VoteObjectDao(BaseDao):
    def __init__(self):
        super().__init__()
        self.TABLE = "raw_vote_object"
        self.COLUMNS = ["id", "blob", "sourceUrl", "sourceType", "format", "isProcessed"]

    def write(self, blob, url):
        if self.isUrlIngested(url):
            logging.info(f"Skipping ingestion of {url}, it's already ingested")
            return 

        c = self.conn.cursor()
        c.execute('''
        INSERT OR IGNORE INTO raw_vote_object 
            (blob, sourceUrl, sourceType, format) 
            VALUES 
            (?, ?, 1, 1);
        ''', (blob, url))
        self.conn.commit()

    def getUnprocessed(self):
        c = self.conn.cursor()
        rows = c.execute('''
        SELECT ro.id, ro.blob, ro.sourceUrl, rs.type, rf.format, ro.isProcessed 
            FROM raw_vote_object ro
            JOIN raw_vote_object_format rf
                ON ro.format = rf.id
            JOIN raw_vote_object_source_type rs
                ON ro.sourceType = rs.id
            WHERE ro.isProcessed = 0
        ''')

        unprocessed = []
        for i in rows:
            voteObject = VoteObject(
                i[1],
                i[2],
                i[3],
                i[4],
                i[5],
            )
            unprocessed.append(voteObject)

        return unprocessed


    def isUrlIngested(self, url):
        c = self.conn.cursor()

        c.execute('''
        SELECT rowid FROM raw_vote_object 
            WHERE sourceUrl = ?
        ''', (url,))

        return c.fetchone() != None
