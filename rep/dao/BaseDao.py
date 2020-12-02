import sqlite3
import logging
from abc import ABC, abstractmethod
from rep.db import sqlite_get_connection_helper

class BaseDao(ABC):
    def __init__(self, **kwargs):
        if 'database' not in kwargs:
            logging.warn("No database supplied, using default connection")
        self.conn = kwargs.get('database', sqlite_get_connection_helper())
    
    @abstractmethod
    def write(self):
        pass
