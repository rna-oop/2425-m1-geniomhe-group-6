from Chain import Chain

class Model:
    def __init__(self, id: int):
        self.id = id
        self._chains = []
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError(f"id must be an integer, got {type(id)}")
        self._id=id
        
    def add_chain(self, chain):
        self._chains.append(chain)
    
    def get_chains(self):
        return self._chains
    
    def remove_chain(self, chain):
        self._chains.remove(chain)
        
    def __repr__(self):
        return f"Model {self.id}"
    
#Example usage
'''
m = Model(1)
print(m) #output: 1
c = Chain("A")
m.add_chain(c)
print(m.get_chains()) #output: [A]
m.remove_chain(c)
print(m.get_chains()) #output: []
'''