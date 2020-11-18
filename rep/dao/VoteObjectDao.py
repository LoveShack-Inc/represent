from dataclasses import dataclass
from rep.dao.BaseDao import BaseDao
from rep.dataclasses.VoteObject import VoteObject
import logging

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

    def getCount(self):
        c = self.conn.cursor()
        rows = c.execute(f'''
        SELECT count(ro.id)
            FROM raw_vote_object ro
        ''')
        return rows.fetchone()[0]

    def getById(self, vote_id):
        c = self.conn.cursor()
        rows = c.execute(f'''
        SELECT ro.id, ro.blob, ro.sourceUrl, rs.type, rf.format, ro.isProcessed 
            FROM raw_vote_object ro
            JOIN raw_vote_object_format rf
                ON ro.format = rf.id
            JOIN raw_vote_object_source_type rs
                ON ro.sourceType = rs.id
            WHERE ro.id = ?
        ''', (vote_id,))
        result = rows.fetchone()
        if result:
            return self._map_row_to_vote_object(result)
        else:
            return None

    def getAll(self, limit=100, offset=0):
        c = self.conn.cursor()
        rows = c.execute(f'''
        SELECT ro.id, ro.blob, ro.sourceUrl, rs.type, rf.format, ro.isProcessed 
            FROM raw_vote_object ro
            JOIN raw_vote_object_format rf
                ON ro.format = rf.id
            JOIN raw_vote_object_source_type rs
                ON ro.sourceType = rs.id
            ORDER BY ro.id LIMIT ? OFFSET ?
        ''', (limit, offset,))
        return [self._map_row_to_vote_object(i) for i in rows]


    def getProcessed(self):
        c = self.conn.cursor()
        rows = c.execute('''
        SELECT ro.id, ro.blob, ro.sourceUrl, rs.type, rf.format, ro.isProcessed 
            FROM raw_vote_object ro
            JOIN raw_vote_object_format rf
                ON ro.format = rf.id
            JOIN raw_vote_object_source_type rs
                ON ro.sourceType = rs.id
            WHERE ro.isProcessed = 1
        ''')
        return [self._map_row_to_vote_object(i) for i in rows]


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

        return [self._map_row_to_vote_object(i) for i in rows]

    def isUrlIngested(self, url):
        c = self.conn.cursor()

        c.execute('''
        SELECT rowid FROM raw_vote_object 
            WHERE sourceUrl = ?
        ''', (url,))

        return c.fetchone() != None

    def _map_row_to_vote_object(self, row):
        return VoteObject(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
        )

