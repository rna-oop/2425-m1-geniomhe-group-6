import os,sys
sys.path.append(os.path.abspath('lab4/src'))

import numpy as np
from Processing.Builder import Builder

class ArrayBuilder(Builder):
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.__array = {}
        self.__sequence = {}
        self.__model_id = 0
        self.__residue_id = 0
        self.__prev_atom=["", 0.0] #[atom_name, occupancy]
        
    @property
    def molecule(self):
        max_atoms_no_per_residue = max((len(atoms) for atoms in self.__array.values()), default=1)
        max_residues_no = max((key[1] for key in self.__array.keys())) + 1
        
        np_array = np.full((self.__model_id + 1, max_residues_no, max_atoms_no_per_residue, 3), np.nan)
        
        for (model_id, residue_id), atoms in self.__array.items():
            for atom_id, coords in enumerate(atoms):
                np_array[model_id, residue_id, atom_id] = coords
                
        np_sequence = np.full((self.__model_id + 1, max_residues_no), "", dtype=object)
        
        for (model_id, residue_id), residue_name in self.__sequence.items():
            np_sequence[model_id, residue_id] = residue_name
            
        self.reset()
        
        return np_sequence, np_array
        
    def add_model(self, model_id):
        if model_id != 0:
            self.__model_id = model_id - 1
        
    def add_chain(self, chain_id):
        pass
    
    def add_residue(self, residue_name, residue_id, i_code):
        self.__residue_id = residue_id -1 
        if (self.__model_id, self.__residue_id) not in self.__array:
            self.__array[(self.__model_id, self.__residue_id)] = []
            self.__sequence[(self.__model_id, self.__residue_id)] = residue_name
            
        
    def add_atom(self, atom_name, x, y, z, element, altloc, occupancy, temp_factor, charge):
        #if a residue contains same atom with different altloc, add the one with the highest occupancy
        if atom_name == self.__prev_atom:
            if occupancy > self.__prev_atom[1]: 
                self.__array[(self.__model_id, self.__residue_id)].append([x, y, z])
                self.__prev_atom=[atom_name, occupancy]
        else:
            self.__array[(self.__model_id, self.__residue_id)].append([x, y, z])
            self.__prev_atom=[atom_name, occupancy]