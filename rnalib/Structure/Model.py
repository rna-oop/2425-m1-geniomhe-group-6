'''
Chain module contains class Chain
'''

import os,sys
# sys.path.append(os.path.abspath('lab3/src'))

from rnalib.Structure.Structure import Structure
from rnalib.Structure.Chain import Chain

class Model(Structure):
    def __init__(self, id: int, chains=None):
        self.id = id
        self._chains = chains if chains is not None else {}
        self.__rna_molecule = None #The Molecule to which the model belongs


    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError(f"id must be an integer, got {type(id)}")
        self._id=id

    @property
    def rna_molecule(self):
        return self.__rna_molecule
    # --again no setter
    def _add_rna_molecule(self, rna_molecule):
        self.__rna_molecule = rna_molecule
    
        
    def add_chain(self, chain):
        if not isinstance(chain, Chain):  
            raise TypeError(f"Expected a Chain instance, got {type(chain)}")
        if chain.id not in self._chains:
            self._chains[chain.id] = chain
            chain._add_model(self)
    
    def get_chains(self):
        return self._chains
    
    def remove_chain(self, chain):
        self._chains.pop(chain.id)
        
    def __repr__(self):
        return f"Model {self.id}"
    
    def accept(self, visitor:'Visitor'):
        visitor.visit_model(self)
    
#Example usage

if __name__ == "__main__":
    m = Model(1)
    print(m) #output: Model 1
    c = Chain("A")
    m.add_chain(c)
    print(m.get_chains()) #output: {'A': A}
    m.remove_chain(c)
    print(m.get_chains()) #output: {}

    # -- e.g. of adding a chain to a model 1-N test (ry)
    c_test=Chain('B')   
    m_test=Model(2)
    m_test.add_chain(c_test)
    print(c_test.model) #Model 2
    # success :)
