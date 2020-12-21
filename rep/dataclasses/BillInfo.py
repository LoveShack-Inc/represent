from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class BillInfo:
    billNum: str
    lcoNum: int
    sessYear: int
    sessNum: int
    typeCode: str
    billTitle: str
    stmtPurp: str
    emergencyCert: bool
    raised: bool
    proposed: bool
    subBill: bool
    nomination: bool
    numPages: int
    houseCalNum: str
    senateCalNum: str
    filedDate: str
    readIntoFloor: str
    petitionNum: str
    pasaNum: int
    pasaType: str
    senateAmd: str
    houseAmd: str
    
    id: int = field(default=None)

