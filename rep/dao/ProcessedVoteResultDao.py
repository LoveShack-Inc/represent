from rep.dao.BaseDao import BaseDao
from rep.dataclasses.ProcessedVoteResult import ProcessedVoteResult
from typing import List


class ProcessedVoteResultDao(BaseDao):
    def __init__(self, **kwargs):
        self.TABLE_NAME = "processed_vote_result"
        super().__init__(**kwargs)

    def _map_result(self, result):
        return ProcessedVoteResult(
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5]
        )

    def write(self, processed_vote_result: ProcessedVoteResult):
        for num, _ in enumerate(processed_vote_result.repVote):
            c = self.conn.cursor()
            tup = (
                processed_vote_result.unixTime,
                processed_vote_result.billNumber,
                processed_vote_result.voteName,
                processed_vote_result.repId[num],
                processed_vote_result.repVote[num],
                processed_vote_result.rawVoteObjectId,
            )
            c.execute('''
                    INSERT OR IGNORE INTO processed_vote_result 
                        (unixTime, billNumber, voteName, repId, repVote, rawVoteObjectId) 
                        VALUES 
                        (?, ?, ?, ?, ?, ?);
                    ''', tup)
            self.conn.commit()

    def getByBillNumber(self, bill_number: str) -> List[ProcessedVoteResult]:
        c = self.conn.cursor()
        rows = c.execute(f'''
            SELECT * FROM {self.TABLE_NAME} pvr
                WHERE pvr.billNumber = ?
        ''', (bill_number,))
        return [self._map_result(i) for i in rows]

    def getByVoteName(self, vote_name: str) -> List[ProcessedVoteResult]:
        c = self.conn.cursor()
        rows = c.execute(f'''
            SELECT * FROM {self.TABLE_NAME} pvr
                WHERE pvr.voteName = ?
        ''', (vote_name,))
        return [self._map_result(i) for i in rows]

    def getByRepId(self, rep_name: int) -> List[ProcessedVoteResult]:
        c = self.conn.cursor()
        rows = c.execute(f'''
            SELECT * FROM {self.TABLE_NAME} pvr
                WHERE pvr.repId = ?
        ''', (rep_id,))
        return [self._map_result(i) for i in rows]

    def getByVoteObjectId(self, rep_name: str) -> List[ProcessedVoteResult]:
        c = self.conn.cursor()
        rows = c.execute(f'''
            SELECT * FROM {self.TABLE_NAME} pvr
                WHERE pvr.rawVoteObjectId = ?
        ''', (rep_name,))
        return [self._map_result(i) for i in rows]
