import logging
from abc import ABC, abstractmethod

class BaseCrawler(ABC):
    def __init__(self):
        self.vote_object_dao = "vote_object_dao"

    @abstractmethod
    def crawl():
        pass
