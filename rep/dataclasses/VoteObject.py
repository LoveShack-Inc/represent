from dataclasses import dataclass, field

@dataclass(frozen=True)
class VoteObject:
    blob: str
    sourceUrl: str
    sourceType: str
    sourceFormat: str
    isProcessed: int
    vote_id: int = field(default=None)
