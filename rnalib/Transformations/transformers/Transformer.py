import os,sys
# sys.path.append(os.path.abspath('lab4/src'))

from abc import ABC, abstractmethod

class Transformer(ABC):
    """
    This class defines the core interface for all transformations. 
    It implements the chain of responsibility pattern, allowing transformers to be linked together.
    Concrete transformer classes must implement the methods defined in this class.
    
    :Methods:
    - set_next: Sets the next transformer in the transformation chain.
    - transform: Performs the transformation on the input data (X, Y).
    """

    @abstractmethod
    def set_next(self, transformer: 'Transformer'):
        pass

    @abstractmethod
    def transform(self, X, Y):
        pass