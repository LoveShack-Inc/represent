from abc import ABC, abstractmethod
import sqlite3


class BaseProcessor(ABC):

    @abstractmethod
    def process_blob(self, blob):
        pass
