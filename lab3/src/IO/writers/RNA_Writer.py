from abc import ABC, abstractmethod

class RNA_Writer(ABC):
    
    @abstractmethod
    def write(self, rna_molecule):
        pass