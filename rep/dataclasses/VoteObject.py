from dataclasses import dataclass

@dataclass
class VoteObject:
    blob: str
    sourceUrl: str
    sourceType: str
    sourceFormat: str
    isProcessed: int
