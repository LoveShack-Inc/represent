from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class ProcessedVoteResult:
    unixTime: int
    billNumber: str
    voteName: str
    repName: List[str]
    repVote: List[str]
    rawVoteObjectId: int

    def validate(self):
        repNameValid = True
        for i in self.repName:
            if i == "":
                repNameValid = False
                break
        repVoteValid = True
        for i in self.repVote:
            if i == "":
                repVoteValid = False
                break

        if (self.billNumber == "" 
            or self.voteName == ""
            or len(self.repName) < 1
            or repNameValid == False
            or len(self.repVote) < 1
            or repVoteValid == False
        ): 
            return False
        else:
            return True

    def __post_init__(self):
        if not self.validate():
            raise ValueError(f"ProcessedVoteResult is invalid:\n\t{self}")

