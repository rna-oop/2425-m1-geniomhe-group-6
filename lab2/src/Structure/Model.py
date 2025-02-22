'''
Chain module contains class Chain
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from Structure.Chain import Chain

class Model:
    def __init__(self, id: int, chains=None):
        self.id = id
        self._chains = chains if chains is not None else {}
        self.rna_molecule = None #The Molecule to which the model belongs


    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError(f"id must be an integer, got {type(id)}")
        self._id=id
        
    def add_chain(self, chain):
        if not isinstance(chain, Chain):  
            raise TypeError(f"Expected a Chain instance, got {type(chain)}")
        if chain.id not in self._chains:
            self._chains[chain.id] = chain
            chain.model = self
    
    def get_chains(self):
        return self._chains
    
    def remove_chain(self, chain):
        self._chains.pop(chain.id)
        
    def __repr__(self):
        return f"Model {self.id}"
    
    
    
#Example usage

if __name__ == "__main__":
    m = Model(1)
    print(m) #output: 1
    c = Chain("A")
    m.add_chain(c)
    print(m.get_chains()) #output: [A]
    m.remove_chain(c)
    print(m.get_chains()) #output: {}
