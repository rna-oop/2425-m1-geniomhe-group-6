from abc import ABC, abstractmethod

class RNA_Parser(ABC):
    
    @abstractmethod
    def read(self, path_to_file):
        pass