import os,sys
sys.path.append(os.path.abspath('lab3/src'))

import numpy as np
from Processing.builders.Builder import Builder

class ArrayBuilder(Builder):
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.__array = {}
        self.__model_id = 0
        self.__residue_id = 0
        
    @property
    def molecule(self):
        np_array = np.zeros((self.__model_id + 1, self.__residue_id + 1, 3))
        for key, value in self.__array.items():
            np_array[key[0], key[1]] = value
        return np_array
        
    def add_model(self, model_id):
        self.__model_id = model_id
        
    def add_chain(self, chain_id):
        pass
    
    def add_residue(self, residue_name, residue_id, i_code):
        self.__residue_id = residue_id
        
    def add_atom(self, atom_name, x, y, z, *args):
        self.__array[(self.__model_id, self.__residue_id)] = [x, y, z]