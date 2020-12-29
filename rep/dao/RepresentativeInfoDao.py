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
            dist=result[0], 
            officeCode=result[1], 
            districtNumber=result[2], 
            designatorCode=result[3], 
            firstName=result[4], 
            middleInitial=result[5], 
            lastName=result[6], 
            suffix=result[7], 
            commonlyUsedName=result[8], 
            homeStreetAddress=result[9], 
            homeCity=result[10], 
            homeState=result[11], 
            homeZipCode=result[12], 
            homePhone=result[13], 
            capitolStreetAddress=result[14], 
            capitolCity=result[15], 
            capitolPhone=result[16], 
            room=result[17], 
            roomNumber=result[18], 
            committeesChaired=result[19], 
            committeesViceChaired=result[20], 
            rankingMember=result[21], 
            committeeMember1=result[22], 
            senatorRepresentative=result[23], 
            party=result[24], 
            title=result[25], 
            gender=result[26], 
            businessPhone=result[27], 
            email=result[28], 
            fax=result[29], 
            prison=result[30], 
            url=result[31], 
            committeeCodes=result[32],
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

    def write(self, representative_info: RepresentativeInfo):
        c = self.conn.cursor()
        tup = (
            representative_info.dist,
            representative_info.officeCode,
            representative_info.districtNumber,
            representative_info.designatorCode,
            representative_info.firstName,
            representative_info.middleInitial,
            representative_info.lastName,
            representative_info.suffix,
            representative_info.commonlyUsedName,
            representative_info.homeStreetAddress,
            representative_info.homeCity,
            representative_info.homeState,
            representative_info.homeZipCode,
            representative_info.homePhone,
            representative_info.capitolStreetAddress,
            representative_info.capitolCity,
            representative_info.capitolPhone,
            representative_info.room,
            representative_info.roomNumber,
            representative_info.committeesChaired,
            representative_info.committeesViceChaired,
            representative_info.rankingMember,
            representative_info.committeeMember1,
            representative_info.senatorRepresentative,
            representative_info.party,
            representative_info.title,
            representative_info.gender,
            representative_info.businessPhone,
            representative_info.email,
            representative_info.fax,
            representative_info.prison,
            representative_info.url,
            representative_info.committeeCodes
        )
        c.execute('''
                INSERT INTO representative_info VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                ''', tup)
        self.conn.commit()
