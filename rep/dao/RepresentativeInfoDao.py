from rep.dao.BaseDao import BaseDao
from rep.dataclasses.RepresentativeInfo import RepresentativeInfo

class RepresentativeInfoDao(BaseDao):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TABLE = "representative_info"
        self.COLUMNS = ["id", "dist", "officeCode", "districtNumber", "number", 
            "designatorCode", "firstName", "middleInitial", "lastName", "suffix", 
            "commonlyUsedName", "homeStreetAddress", "homeCity", "homeState", 
            "homeZipCode", "homePhone", "capitolStreetAddress", "capitolCity", 
            "capitolPhone", "room", "roomNumber", "committeesChaired", 
            "committeesViceChaired", "rankingMember", "committeeMember1", 
            "senatorRepresentative", "party", "title", "gender", "businessPhone", 
            "email", "fax", "prison", "url", "committeeCodes"]

    def _map_result(self, result):
        return RepresentativeInfo(
            id=result[0],
            dist=result[0], 
            officeCode=result[1], 
            districtNumber=result[2], 
            number=result[3], 
            designatorCode=result[4], 
            firstName=result[5], 
            middleInitial=result[6], 
            lastName=result[7], 
            suffix=result[8], 
            commonlyUsedName=result[9], 
            homeStreetAddress=result[10], 
            homeCity=result[11], 
            homeState=result[12], 
            homeZipCode=result[13], 
            homePhone=result[14], 
            capitolStreetAddress=result[15], 
            capitolCity=result[16], 
            capitolPhone=result[17], 
            room=result[18], 
            roomNumber=result[19], 
            committeesChaired=result[20], 
            committeesViceChaired=result[21], 
            rankingMember=result[22], 
            committeeMember1=result[23], 
            senatorRepresentative=result[24], 
            party=result[25], 
            title=result[26], 
            gender=result[27], 
            businessPhone=result[28], 
            email=result[29], 
            fax=result[30], 
            prison=result[31], 
            url=result[32], 
            committeeCodes=result[33]
            result=[34]
        )


    def _get_id_from_name(self, name):
        representatives = self.getAll()
        hi = 0


    def getAll(self):
        c = self.conn.cursor()
        c.execute('''SELECT * FROM representative_info;''')
        rows = c.fetchall()
        self.conn.commit()
        representatives = [self._map_result(row) for row in rows]
        return representatives

    def write(self):
        pass
