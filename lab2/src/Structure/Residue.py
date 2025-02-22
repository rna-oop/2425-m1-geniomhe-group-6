'''
Residue module containing class Residue and enum NBase
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from enum import Enum
from Structure.Atom import Atom

class NBase(Enum):
    G = "G"
    A = "A"
    C = "C"
    U = "U"


class Residue:

    def __init__(self, type: str, position: int, atoms=None):
        self.type = type
        self.position = position
        self._atoms = atoms if atoms is not None else {}  
        self.chain = None #The chain to which the residue belongs

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        if not isinstance(type, str):
            raise TypeError(f"type must be a string, got {type(type)}")
        if not type in NBase.__members__:
            raise ValueError(f"{type} is not a valid NBase value")
        self._type=NBase.__members__[type]

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        if not isinstance(position, int):
            raise TypeError(f"position must be an integer, got {type(position)}")
        self._position=position

    def add_atom(self, atom):
        if not isinstance(atom, Atom):
            raise TypeError(f"Expected an Atom instance, got {type(atom)}")
        if (atom.name.value, atom.altloc) not in self._atoms:
            self._atoms[(atom.name.value, atom.altloc)] = atom
            atom.residue = self

    def get_atoms(self):
        return self._atoms
    
    def remove_atom(self, atom):
        self._atoms.pop((atom.name.value, atom.altloc))

    def __repr__(self):
        return f"Residue type:{self.type.value} position:{self.position}"


#Example usage

if __name__ == "__main__":
    
    r = Residue("A", 1)
    print(r) #output: Residue type:A position:1
    atom1 = Atom("C1'", 1.0, 2.0, 3.0, "C")
    atom2 = Atom("N9", 4.0, 5.0, 6.0, "N")
    r.add_atom(atom1)
    r.add_atom(atom2)
    print(r.get_atoms()) #output: {("C1'", None): AtomName.C1_prime 1.0 2.0 3.0 Element.C, ('N9', None): AtomName.N9 4.0 5.0 6.0 Element.N}
    r.remove_atom(atom1)
    print(r.get_atoms()) #output: {('N9', None): AtomName.N9 4.0 5.0 6.0 Element.N}

    atom3 = Atom("C4", 7.0, 8.0, 9.0, "C")
    r2 = Residue("G", 2)
    r2.add_atom(atom3)
    print(r2.get_atoms()) #output: {('C4', None): AtomName.C4 7.0 8.0 9.0 Element.C}
    r2.add_atom(atom3) 
    print(r2.get_atoms()) #output: {('C4', None): AtomName.C4 7.0 8.0 9.0 Element.C}