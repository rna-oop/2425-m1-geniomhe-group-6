
import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from Structure.Residue import Residue

class Chain:
    def __init__(self, id: str, residues=None):
        self.id = id
        self._residues = residues if residues is not None else {}

        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if not isinstance(id, str):
            raise TypeError(f"id must be a string, got {type(id)}")
        self._id=id
        
    def add_residue(self, residue):
        if not isinstance(residue, Residue):
            raise TypeError(f"Expected a Residue instance, got {type(residue)}")
        if residue.position not in self._residues:
            self._residues[residue.position] = residue
            residue.chain = self
        
    def get_residues(self):
        return self._residues
    
    def remove_residue(self, residue):
        self._residues.pop(residue.position)
        
    def __repr__(self):
        return f"Chain {self.id}"


#Example usage

if __name__ == "__main__":
    c = Chain("A")
    print(c) #output: Chain A
    r = Residue("A", 1)
    c.add_residue(r)
    print(c.get_residues()) #output: {1: A 1}
    c.remove_residue(r)
    print(c.get_residues()) #output: {}
