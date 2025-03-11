import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from Processing.builders.Builder import Builder

class Director:
    
    def __init__(self):
        self.__builder = None
        
    @property
    def builder(self):
        return self.__builder
    
    @builder.setter
    def builder(self, builder):
        if not isinstance(builder, Builder):
            raise ValueError("The builder must be an instance of a Builder class.")
        self.__builder=builder
        
    def add_atom_info(self, model_id, *atom_info):
        atom_name, x, y, z, element, residue_name, residue_id, chain_id, altloc, occupancy, temp_factor, i_code, charge = atom_info
        self.builder.add_model(model_id)
        self.builder.add_chain(chain_id)
        self.builder.add_residue(residue_name, residue_id, i_code)
        self.builder.add_atom(atom_name, x, y, z, element, altloc, occupancy, temp_factor, charge)
        
        