from enum import Enum
from Atom import Atom

class NBase(Enum):
    G = "G"
    A = "A"
    C = "C"
    T = "T"


class Residue:

    def __init__(self, type: str, position: int):
        self.type = type
        self.position = position
        self._atoms = []

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
        self._atoms.append(atom)

    def get_atoms(self):
        return self._atoms
    
    def remove_atom(self, atom):
        self._atoms.remove(atom)

    def __repr__(self):
        return f"{self.type.name} {self.position}"


#Example usage
'''
r = Residue("A", 1)
print(r) #output: A 1
atom1 = Atom("C1'", 1.0, 2.0, 3.0, "C")
atom2 = Atom("N9", 4.0, 5.0, 6.0, "N")
r.add_atom(atom1)
r.add_atom(atom2)
print(r.get_atoms()) #output: [C1' 1.0 2.0 3.0 C, N9 4.0 5.0 6.0 N]
r.remove_atom(atom1)
print(r.get_atoms()) #output: [N9 4.0 5.0 6.0 N]
'''
