import sqlite3
from abc import ABC, abstractmethod

class BaseDao(ABC):
    def __init__(self):
        self.conn = sqlite3.connect('./database/db.sqlite')
    
    @abstractmethod
    def write():
        pass
