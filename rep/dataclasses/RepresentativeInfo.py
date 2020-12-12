from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class RepresentativeInfo:
    firstName: str
    middleName: str
    lastName: str
    fullName: str
    state: str
    party: str
    
    id: int = field(default=None)

    def validate(self):

        if (self.lastName == "" 
            or self.state == ""
        ): 
            return False
        else:
            return True

    def __post_init__(self):
        if not self.validate():
            raise ValueError(f"RepresentativeInfo is invalid:\n\t{self}")

