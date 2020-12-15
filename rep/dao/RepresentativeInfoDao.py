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
            dist=result[1], 
            officeCode=result[2], 
            districtNumber=result[3], 
            number=result[4], 
            designatorCode=result[5], 
            firstName=result[6], 
            middleInitial=result[7], 
            lastName=result[8], 
            suffix=result[9], 
            commonlyUsedName=result[10], 
            homeStreetAddress=result[11], 
            homeCity=result[12], 
            homeState=result[13], 
            homeZipCode=result[14], 
            homePhone=result[15], 
            capitolStreetAddress=result[16], 
            capitolCity=result[17], 
            capitolPhone=result[18], 
            room=result[19], 
            roomNumber=result[20], 
            committeesChaired=result[21], 
            committeesViceChaired=result[22], 
            rankingMember=result[23], 
            committeeMember1=result[24], 
            senatorRepresentative=result[25], 
            party=result[26], 
            title=result[27], 
            gender=result[28], 
            businessPhone=result[29], 
            email=result[30], 
            fax=result[31], 
            prison=result[32], 
            url=result[33], 
            committeeCodes=result[34]
        )


    def _get_id_from_name(self, name):
        rows = self.getAll()
        representatives = [self._map_result(row) for row in rows]
        hi = 0


    def getAll(self):
        c = self.conn.cursor()
        c.execute('''SELECT * FROM representative_info;''')
        rows = c.fetchall()
        self.conn.commit()
        return rows

    def write(self):
        pass
