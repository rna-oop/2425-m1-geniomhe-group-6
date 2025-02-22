'''
Atom module contains class Atom and two enums Element and AtomName
'''

from enum import Enum

#Define the Element enum
class Element(Enum):
    C = "C"
    O = "O"
    N = "N"
    P = "P"


#Define the AtomName enum
class AtomName(Enum):
    #Ribose atoms
    C1_prime = "C1'"
    C2_prime = "C2'"
    C3_prime = "C3'"
    C4_prime = "C4'"
    C5_prime = "C5'"
    O2_prime = "O2'"
    O3_prime = "O3'"
    O4_prime = "O4'"
    O5_prime = "O5'"
    #Phosphate atoms
    P = "P"
    OP1 = "OP1"
    OP2 = "OP2"
    OP3 = "OP3"
    #Base atoms
    N1 = "N1"
    N3 = "N3"
    N7 = "N7"
    N9 = "N9"
    C2 = "C2"
    C4 = "C4"
    C5 = "C5"
    C6 = "C6"
    N6 = "N6"
    N2 = "N2"
    O6 = "O6"
    C8 = "C8"
    N4 = "N4"
    O2 = "O2"
    O4 = "O4"

atom_name_lookup = {atom.value: atom for atom in AtomName} #To look for the AtomName enum by its value

class Atom:

    def __init__(self, name: str, x: float, y: float, z: float, element: str, altloc=None, occupancy=None, temp_factor=None, i_code=None, charge=None):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.element = element
        self.altloc = altloc
        self.occupancy = occupancy
        self.temp_factor = temp_factor
        self.i_code = i_code
        self.charge = charge
        self.residue = None #The residue to which the atom belongs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError(f"atom_name must be a string, got {type(name)}")
        #Check if the string is a valid AtomName
        if not name in atom_name_lookup:
            raise ValueError(f"{name} is not a valid AtomName value")
        self._name=atom_name_lookup[name]

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        if not isinstance(element, str):
            raise TypeError(f"element must be a string, got {type(element)}")
        #Check if the string is a valid Element
        if not element in Element.__members__:
            raise ValueError(f"{element} is not a valid Element value")
        self._element=Element.__members__[element]
        
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError(f"x must be a number, got {type(x)}")
        self._x=x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if not isinstance(y, (int, float)):
            raise TypeError(f"y must be a number, got {type(y)}")
        self._y=y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        if not isinstance(z, (int, float)):
            raise TypeError(f"z must be a number, got {type(z)}")
        self._z=z
        

    @property
    def altloc(self):
        return self._altloc
    
    @altloc.setter
    def altloc(self, altloc):
        if altloc is not None and not isinstance(altloc, str):
            raise TypeError(f"altloc must be a string, got {type(altloc)}")
        self._altloc=altloc
        
    @property
    def occupancy(self):
        return self._occupancy
    
    @occupancy.setter
    def occupancy(self, occupancy):
        if occupancy is not None and not isinstance(occupancy, float):
            raise TypeError(f"occupancy must be a float, got {type(occupancy)}")
        self._occupancy=occupancy
        
        
    @property
    def temp_factor(self):
        return self._temp_factor
    
    @temp_factor.setter
    def temp_factor(self, temp_factor):
        if temp_factor is not None and not isinstance(temp_factor, float):
            raise TypeError(f"temp_factor must be a float, got {type(temp_factor)}")
        self._temp_factor=temp_factor
        
    @property
    def i_code(self):
        return self._i_code
    
    @i_code.setter
    def i_code(self, i_code):
        if i_code is not None and not isinstance(i_code, str):
            raise TypeError(f"i_code must be a string, got {type(i_code)}")
        self._i_code=i_code
        
    @property
    def charge(self):
        return self._charge
    
    @charge.setter
    def charge(self, charge):
        if charge is not None and not isinstance(charge, str):
            raise TypeError(f"charge must be a string, got {type(charge)}")
        self._charge=charge

        
    def __repr__(self):
        return f"{self.name} {self.x} {self.y} {self.z} {self.element}"


#Example usage

if __name__ == "__main__":
    atom = Atom("C1'", 1.0, 2.0, 3.0, "C")
    print(atom) #output: C1' 1.0 2.0 3.0 C
