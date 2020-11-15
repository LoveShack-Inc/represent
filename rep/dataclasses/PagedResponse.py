from math import ceil
from dataclasses import dataclass, field

@dataclass
class PagedResponse:
    resources: list
    currentPage: int
    pageSize: int
    totalCount: int
    nextPage: int = field(init=False)
    totalPages: int = field(init=False)

    def __post_init__(self):
        self.nextPage = self._nextPage()
        self.totalPages = self._totalPages()

    def _totalPages(self) -> int:
        return ceil(self.totalCount / self.pageSize) - 1
    
    def _nextPage(self) -> int:
        nextPage = None

        hasNextPage = self.totalCount >= ((self.currentPage + 1) * self.pageSize)
        if hasNextPage:
            nextPage = self.currentPage + 1

        return nextPage

