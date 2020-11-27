import sqlite3
from abc import ABC, abstractmethod
from rep.db import sqlite_get_connection_helper

class BaseDao(ABC):
    def __init__(self):
        self.conn = sqlite_get_connection_helper() 
    
    @abstractmethod
    def write(self):
        pass
