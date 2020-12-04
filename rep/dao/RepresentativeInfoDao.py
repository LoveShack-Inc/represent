from rep.dao.BaseDao import BaseDao
from rep.dataclasses.RepresentativeInfo import RepresentativeInfo

class RepresentativeInfoDao(BaseDao):
    def __init__(self, **kwargs):
        self.TABLE_NAME = "representative_info"
        super().__init__(**kwargs)

    def _map_result(self, result):
        return RepresentativeInfo(
            result[0],
            result[1],
            result[2],
            result[3],
            result[4]
        )

    def write(self, name, state):
        split_name = name.split(' ')
        if len(split_name) == 1:
            


        c = self.conn.cursor()
        tup = (
            representative_info.firstName,
            representative_info.middleName,
            representative_info.lastName,
            representative_info.state,
            representative_info.party,
        )
        c.execute('''
                INSERT OR IGNORE INTO representative_info
                    (firstName, middleName, lastName, state, party) 
                    VALUES 
                    (?, ?, ?, ?, ?);
                ''', tup)
        self.conn.commit()
