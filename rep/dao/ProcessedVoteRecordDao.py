from rep.dao.BaseDao import BaseDao


class ProcessedVoteRecordDao(BaseDao):
    def __init__(self):
        super().__init__()

    def mark_processed(self, source_url):
        tuple_source_url = (source_url,)
        c = self.conn.cursor()
        c.execute('''
                    UPDATE raw_vote_object
                        SET isProcessed='1'
                        WHERE sourceUrl=?;
                        ''', tuple_source_url)
        self.conn.commit()

    def write(self, unixTime, billNumber, voteName, repName, repVote):
        for num, _ in enumerate(repVote):
            c = self.conn.cursor()
            c.execute('''
                    INSERT OR IGNORE INTO processed_vote_result 
                        (unixTime, billNumber, voteName, repName, repVote) 
                        VALUES 
                        (?, ?, ?, ?, ?);
                    ''', (unixTime, billNumber, voteName, repName[num], repVote[num]))
            self.conn.commit()
