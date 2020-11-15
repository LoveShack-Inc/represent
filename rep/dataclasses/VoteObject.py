from dataclasses import dataclass

@dataclass(frozen=True)
class VoteObject:
    vote_id: int
    blob: str
    sourceUrl: str
    sourceType: str
    sourceFormat: str
    isProcessed: int
