from abc import ABC, abstractmethod

import os,sys
# sys.path.append(os.path.abspath('lab3/src'))

class Structure(ABC):
    '''
    abstract class defined in order to build the _Visitor_ design pattern
    >meant to be inherted by:
    - *RNA_Molecule* class
    - *Model* class
    - *Chain* class
    - *Residue* class
    - *Atom* class
    and enforces the implementation of the *accept* method

    - abstract methods:
        accept(visitor) -> None
    '''

    @abstractmethod
    def accept(self, visitor:'Visitor'):
        '''
        abstract method that is meant to be implemented by the classes that inherit from Structure;  
        allows the visitor to visit the class that implements this method
        '''
        pass

