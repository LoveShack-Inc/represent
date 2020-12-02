from dataclasses import dataclass, field

@dataclass(frozen=True)
class VoteObjectFilter:
    sourceUrl: str = field(default=None)
    sourceType: str = field(default=None)
    sourceFormat: str = field(default=None)
    isProcessed: int = field(default=None)
    vote_id: int = field(default=None)

    def validate(self) -> bool:
        """
            Filter is useless if every filterable field is None
        """
        if (self.sourceUrl is None 
            and self.sourceType is None
            and self.sourceFormat is None
            and self.isProcessed is None
            and self.vote_id is None):
            return False
        else:
            return True
    
    def __post_init__(self):
        if not self.validate():
            raise ValueError("VoteObjectFilter is invalid, at least one filter must be specified")
