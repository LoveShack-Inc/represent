from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class RepresentativeInfo:
    dist: str 
    officeCode: str 
    districtNumber: str 
    designatorCode: str 
    firstName: str 
    middleInitial: str 
    lastName: str 
    suffix: str 
    commonlyUsedName: str 
    homeStreetAddress: str 
    homeCity: str 
    homeState: str 
    homeZipCode: str 
    homePhone: str 
    capitolStreetAddress: str 
    capitolCity: str 
    capitolPhone: str 
    room: str 
    roomNumber: str 
    committeesChaired: str 
    committeesViceChaired: str 
    rankingMember: str 
    committeeMember1: str 
    senatorRepresentative: str 
    party: str 
    title: str 
    gender: str 
    businessPhone: str 
    email: str 
    fax: str 
    prison: str 
    url: str 
    committeeCodes: str
    
    id: int = field(default=None)

