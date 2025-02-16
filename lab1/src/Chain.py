from Residue import Residue

class Chain:
    def __init__(self, id: str):
        self.id = id
        self._residues = []
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if not isinstance(id, str):
            raise TypeError(f"id must be a string, got {type(id)}")
        self._id=id
        
    def add_residue(self, residue):
        self._residues.append(residue)
        
    def get_residues(self):
        return self._residues
    
    def remove_residue(self, residue):
        self._residues.remove(residue)
        
    def __repr__(self):
        return f"{self.id}"


#Example usage
'''
c = Chain("A")
print(c) #output: A
r = Residue("A", 1)
c.add_residue(r)
print(c.get_residues()) #output: [A 1]
c.remove_residue(r)
print(c.get_residues()) #output: []
'''