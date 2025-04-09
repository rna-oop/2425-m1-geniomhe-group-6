import os,sys
# sys.path.append(os.path.abspath('lab3/src'))

from abc import ABC, abstractmethod

class Builder(ABC):
    """
    The Builder interface declares a set of methods to assemble an RNA molecule.
    """

    @property
    @abstractmethod
    def molecule(self):
        pass
    
    @abstractmethod
    def add_atom(self):
        pass
    
    @abstractmethod
    def add_residue(self):
        pass
    
    @abstractmethod
    def add_chain(self):
        pass
    
    @abstractmethod
    def add_model(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass
    
    