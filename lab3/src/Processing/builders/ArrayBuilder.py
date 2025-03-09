import os,sys
sys.path.append(os.path.abspath('lab3/src'))

import numpy as np

class ArrayBuilder:
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.__array = []
        self.__model_id = 0
        self.__residue_id = 0
        
    @property
    def molecule(self):
        array = self.__array
        self.reset()
        return np.array(array)
        
    def add_model(self, model_id):
        self.__model_id = model_id
        
    def add_chain(self, chain_id):
        pass
    
    def add_residue(self, residue_name, residue_id, i_code):
        self.__residue_id = residue_id
        
    def add_atom(self, atom_name, x, y, z, *args):
        self.__array[[self.__model_id, self.__residue_id]] = [x,y,z]