from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    @abstractmethod
    def process_blob(self, blob):
        pass
