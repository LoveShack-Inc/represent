from dataclasses import dataclass, asdict
from rep.dataclasses.VoteObjectFilter import VoteObjectFilter
from rep.dao.BaseDao import BaseDao
from rep.dataclasses.VoteObject import VoteObject
from rep.dataclasses.Enums import SourceFormat, SourceType
import logging

DEFAULT_PAGE_SIZE = 100
DEFAULT_OFFSET = 0

class VoteObjectDao(BaseDao):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TABLE = "raw_vote_object"
        self.COLUMNS = ["id", "blob", "sourceUrl", "sourceType", "format", "isProcessed"]

    def _make_filterable(self, q_filter: VoteObjectFilter, query_string: str, query_named_params: dict) -> (str, dict):
        if q_filter is not None:
            # the filter dataclass won't build if there are no filters present, so we can safely add
            # the "WHERE" condition here and assume at least one filter is being used
            query_string += "WHERE 1=1"
            if q_filter.sourceType is not None:
                query_string += " AND rs.type = :source_type"
                query_named_params["source_type"] = q_filter.sourceType
            if q_filter.sourceFormat is not None:
                query_string += " AND rf.format = :source_format"
                query_named_params["source_format"] = q_filter.sourceFormat
            if q_filter.sourceUrl is not None:
                query_string += " AND ro.sourceUrl = :source_url"
                query_named_params["source_url"] = q_filter.sourceUrl
            if q_filter.isProcessed is not None:
                query_string += " AND ro.isProcessed = :is_processed"
                query_named_params["is_processed"] = q_filter.isProcessed

        return query_string, query_named_params

    def write(self, vote_object: VoteObject):
        if self.isUrlIngested(vote_object.sourceUrl):
            logging.info(f"Skipping ingestion of {vote_object.sourceUrl}, it's already ingested")
            return 

        c = self.conn.cursor()
        c.execute('''
        INSERT OR IGNORE INTO raw_vote_object 
            (blob, sourceUrl, sourceType, format) 
            VALUES 
            (?, ?, ?, ?);
        ''', (vote_object.blob, vote_object.sourceUrl, SourceType[vote_object.sourceType].value, SourceFormat[vote_object.sourceFormat].value,))
        self.conn.commit()

    def getCount(self, q_filter: VoteObjectFilter=None):
        c = self.conn.cursor()

        base_query = '''
            SELECT count(ro.id)
                FROM raw_vote_object ro
        '''
        full_query, query_named_params = self._make_filterable(q_filter, base_query, {})
        rows = c.execute(full_query, query_named_params)
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

    def getAll(self, limit=DEFAULT_PAGE_SIZE, offset=DEFAULT_OFFSET, q_filter: VoteObjectFilter=None):
        c = self.conn.cursor()
        base_query = '''
        SELECT ro.id, ro.blob, ro.sourceUrl, rs.type, rf.format, ro.isProcessed 
            FROM raw_vote_object ro
            JOIN raw_vote_object_format rf
                ON ro.format = rf.id
            JOIN raw_vote_object_source_type rs
                ON ro.sourceType = rs.id
        '''

        query_named_params = {
            "offset": offset,
            "limit": limit
        }

        base_query, query_named_params = self._make_filterable(q_filter, base_query, query_named_params)

        full_query = f'''
            {base_query}
            ORDER BY ro.id LIMIT :limit OFFSET :offset
        '''

        logging.debug(f"{full_query}, {query_named_params}")
        rows = c.execute(full_query, query_named_params)
        return [self._map_row_to_vote_object(i) for i in rows]


    def getProcessed(self, limit=DEFAULT_PAGE_SIZE, offset=DEFAULT_OFFSET):
        c = self.conn.cursor()
        rows = c.execute('''
        SELECT ro.id, ro.blob, ro.sourceUrl, rs.type, rf.format, ro.isProcessed 
            FROM raw_vote_object ro
            JOIN raw_vote_object_format rf
                ON ro.format = rf.id
            JOIN raw_vote_object_source_type rs
                ON ro.sourceType = rs.id
            WHERE ro.isProcessed = 1
            ORDER BY ro.id LIMIT ? OFFSET ?
        ''', (limit, offset,))
        return [self._map_row_to_vote_object(i) for i in rows]


    def markProcessedBySourceUrl(self, source_url):
        c = self.conn.cursor()
        c.execute('''
                    UPDATE raw_vote_object
                        SET isProcessed='1'
                        WHERE sourceUrl=?;
                        ''', (source_url,))
        self.conn.commit()


    def getUnprocessed(self, limit=DEFAULT_PAGE_SIZE, offset=DEFAULT_OFFSET):
        c = self.conn.cursor()
        rows = c.execute('''
        SELECT ro.id, ro.blob, ro.sourceUrl, rs.type, rf.format, ro.isProcessed 
            FROM raw_vote_object ro
            JOIN raw_vote_object_format rf
                ON ro.format = rf.id
            JOIN raw_vote_object_source_type rs
                ON ro.sourceType = rs.id
            WHERE ro.isProcessed = 0
                AND ro.sourceUrl like '%VOTE%'
            ORDER BY ro.id LIMIT ? OFFSET ?
        ''', (limit, offset,))

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
            vote_id=row[0],
            blob=row[1],
            sourceUrl=row[2],
            sourceType=row[3],
            sourceFormat=row[4],
            isProcessed=row[5],
        )

