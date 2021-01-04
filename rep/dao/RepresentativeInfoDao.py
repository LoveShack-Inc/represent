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
        )


    def get_id_from_name(self, name):
        reps = self.getAll()
        # I'm not sure if this is the cleanest and most robust way to do name lookups.
        # It's complicated by the fact that we don't know if we're getting 
        # full names or just last names. 
        for rep in reps:
            if rep.lastName.upper() in name.upper():
                return rep.id
        return -1


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
