'''
Atom module contains class Atom and two enums Element and AtomName
'''

from RNAr.Structure.Structure import Structure
from enum import Enum

#Define the Element enum
class Element(Enum):
    C = "C"
    O = "O"
    N = "N"
    P = "P"
    H = "H"

class Atom(Structure):

    def __init__(self, name: str, x: float, y: float, z: float, element: str, altloc=None, occupancy=None, temp_factor=None, charge=None):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.element = element
        self.altloc = altloc
        self.occupancy = occupancy
        self.temp_factor = temp_factor
        self.charge = charge
        self.__residue = None #The residue to which the atom belongs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError(f"atom_name must be a string, got {type(name)}")
        self._name=name

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
    def charge(self):
        return self._charge
    
    @charge.setter
    def charge(self, charge):
        if charge is not None and not isinstance(charge, str):
            raise TypeError(f"charge must be a string, got {type(charge)}")
        self._charge=charge

        
    def __repr__(self):
        return f"{self.name} {self.x} {self.y} {self.z} {self.element}"
    
    @property
    def residue(self):
        return self.__residue
    #no setter will be implemented for this attribute, it will be set directly

    # -- as is the case in classes in Families module, 
    # to handle this 1-N relationship we need to add a residue attribute only when an atom instance is added to a residue instance
    # for that we'll create a helper method

    def _add_residue(self, residue):
        '''
        helper function to add an Atom to the residue object when it is used in the Residue module

        the user must always add an Atom from a residue instance and addition to the Atom instance will be done automatically
        '''
        # --no need to validate Residue since this method will be called from Residue class method on self (being of type Residue is inevitable)
        self.__residue = residue 


    def accept(self, visitor:'Visitor'):
        visitor.visit_atom(self)
        
#Example usage

if __name__ == "__main__":
    atom = Atom("C1'", 1.0, 2.0, 3.0, "C")
    print(atom) #output: C1' 1.0 2.0 3.0 C
