from rep.dao.BaseDao import BaseDao
from rep.dataclasses.BillInfo import BillInfo

class BillInfoDao(BaseDao):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TABLE = "bill_info"
        self.COLUMNS = ["billNum", "lcoNum", "sessYear", "sessNum", "typeCode", 
        "billTitle", "stmtPurp", "emergencyCert", "raised", "proposed", 
        "subBill", "nomination", "numPages", "houseCalNum", "senateCalNum", 
        "filedDate", "readIntoFloor", "petitionNum", "pasaNum", "pasaType", 
        "senateAmd", "houseAmd"]

    def _map_result(self, result):
        return BillInfo(
            id=result[0],
            billNum=result[1],
            lcoNum=result[2],
            sessYear=result[3],
            sessNum=result[4],
            typeCode=result[5],
            billTitle=result[6],
            stmtPurp=result[7],
            emergencyCert=result[8],
            raised=result[9],
            proposed=result[10],
            subBill=result[11],
            nomination=result[12],
            numPages=result[13],
            houseCalNum=result[14],
            senateCalNum=result[15],
            filedDate=result[16],
            readIntoFloor=result[17],
            petitionNum=result[18],
            pasaNum=result[19],
            pasaType=result[20],
            senateAmd=result[21],
            houseAmd=result[22]
        )


    def getAll(self):
        c = self.conn.cursor()
        c.execute('''SELECT * FROM bill_info;''')
        rows = c.fetchall()
        self.conn.commit()
        bills = [self._map_result(row) for row in rows]
        return bills

    def write(self):
        pass
