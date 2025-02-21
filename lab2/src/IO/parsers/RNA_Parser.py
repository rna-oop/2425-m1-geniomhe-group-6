'''
RNA_Parser is an abstract class that defines the interface for all RNA parsers (a child is PDB_Parser)
'''

from abc import ABC, abstractmethod

class RNA_Parser(ABC):
    
    @abstractmethod
    def read(self, path_to_file):
        pass