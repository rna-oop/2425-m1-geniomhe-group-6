'''
module processor contains class Processor for handling parse/write operations (helper)
'''

import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from Structure.RNA_Molecule import RNA_Molecule
from Structure.Model import Model
from Structure.Chain import Chain
from Structure.Residue import Residue
from Structure.Atom import Atom
from Families.species import Species

import numpy as np

import xml.etree.ElementTree as ET
from xml.dom import minidom

#-- helpers

def pretty_print_xml(func): #--used as decorator
    def wrapper(*args, **kwargs):
        xml_string = func(*args, **kwargs)
            
        dom = minidom.parseString(xml_string)
            
        pretty_xml = dom.toprettyxml(indent="  ")
            
        return pretty_xml
    return wrapper

def max_occupancy(atom1,atom2):
    '''takes 2 atoms (supposedly same atoms on alt locations) and returns the one with highest occupancy'''
    if atom1[9]>atom2[9]: #occupancy saved as 9th element in the atom list rep
        return atom1
    else:
        return atom2

class Processor:
    
    def __init__(self):
        self.entry_id = None
        self.experiment = None
        self.species = None
        self.rna_molecule = None
        self.atoms = []
        
    def molecule_info(self, entry_id, experiment, species):
        self.entry_id = entry_id
        if experiment is not None:
            self.experiment = experiment
        if species is not None:
            self.species = Species(species)
        
    def atom_info(self, *args):
        self.atoms.append(list(args))
        
    def createMolecule(self):
        '''
        Creates an RNA molecule object from the parsed information.
        '''
        
        self.rna_molecule = RNA_Molecule(self.entry_id, self.experiment, self.species)
        
        for atom in self.atoms:
            
            atom_name, x, y, z, element, residue_name, residue_id, chain_id, altloc, occupancy, temp_factor, i_code, charge, model_id = atom
            
            self.rna_molecule.add_model(Model(model_id))
            model = self.rna_molecule.get_models()[model_id]
            model.add_chain(Chain(chain_id))
            chain = model.get_chains()[chain_id]
            chain.add_residue(Residue(residue_name, residue_id, i_code=i_code))
            residue = chain.get_residues()[residue_id]
            residue.add_atom(Atom(atom_name, x, y, z, element, altloc, occupancy, temp_factor, charge))
                
        return self.rna_molecule
    
    def createArray(self):
        '''
        Creates an array representation of the RNA molecule.
        The array has dimensions (number of models, max_residues_no, max_atoms_per_residue_no, 3) and stores the x,y,z coordinates of each atom.
        Empty cells are filled with nan.
        '''
        #--get the max no of models
        max_models_no=max(self.atoms[-1][-1], 1) #check the the model_id of the last atom
        
        #--get the max no of residues and atoms per residue
        max_residues_no=0
        max_atoms_per_residue_no=0
        
        current_residue_id=0
        current_atoms_no=0
        current_atom_name=""
        
        for atom in self.atoms:
            
            #get the max no of residues
            if atom[6] > max_residues_no:
                max_residues_no=atom[6]
                
            if atom[6]!=current_residue_id: #if new residue
                current_residue_id=atom[6]
                current_atoms_no=0 #reset the current atoms no
            
            if current_atom_name!=atom[0]: #increment the current atoms no only if the atom name is different
                current_atom_name=atom[0]
                current_atoms_no += 1

            #get the max no of atoms per residue
            if current_atoms_no > max_atoms_per_residue_no: 
                max_atoms_per_residue_no=current_atoms_no
                
        #--initialize the array with nan
        array=np.full((max_models_no, max_residues_no, max_atoms_per_residue_no, 3), np.nan) 
        
        #--fill the array with the coordinates
        current_residue_id=0
        current_atom_id=0
        current_atom_name=""
        prev_atom=None
        
        for atom in self.atoms:
            
            model_id=max(atom[-1]-1, 0) #model_id starts from 1, array index starts from 0
            
            if atom[6]!=current_residue_id: #if new residue
                current_residue_id=atom[6]
                current_atom_id=0 #reset the current atom id
                prev_atom=None
                current_atom_name=""
            
            if current_atom_name!=atom[0]: 
                current_atom_id += 1
                array[model_id, current_residue_id-1,  current_atom_id-1]=np.array(atom[1:4]) #store the x,y,z coordinates in the array
                prev_atom=atom
                
            if current_atom_name==atom[0]:
                a=max_occupancy(atom, prev_atom)
                array[model_id, current_residue_id-1,  current_atom_id-1]=np.array(a[1:4]) 
                prev_atom=a
                
            current_atom_name=atom[0]
            
        return array
        
    def flattenMolecule(self, rna_molecule):
        """
        Flattens the RNA molecule into a list of atoms.
        Each atom is a tuple containing the model ID, serial number, atom, residue and chain.
        """
        atoms = []
        model_id=0
        for model in rna_molecule.get_models().values():
            model_id = model.id
            serial=1
            for chain in model.get_chains().values():
                for residue in chain.get_residues().values():
                    for atom in residue.get_atoms().values():
                        atoms.append((model_id, serial, atom, residue, chain))
                        serial += 1
        return atoms

    def flattenArray(self, array):
        '''
        takes a 3D array RNA Molecule representation (as prviously defined)
        returns a list of atoms

        parameters:
        
        array: numpy array, (3D) dimensions should be 
            - number of models
            - number of residues
            - 3 (values should be each atom's x,y,z coordinates)

        returns:
        
        atoms: list of tuples, each tuple contains 
            - the model ID (default)
            - serial number (index)
            - atom (unknown, X, maybe can add index like X1, X2, etc) in any case here the nth atom is of form [Xn, [x,y,z]] and not an Atom object
            - residue (unkown, UNK) 
            - chain (default, until gaps are introduced)
        '''

        # --removing the initialized 1st nul atom, comment it if array has no longer a nul atom
        if np.all(array[:,0,:]==[0,0,0]):
            array=array[:,1:,:]

        atoms = []
        model_id=0
        chain='X'
        residue='UNK' #or blanks in pdb
        residue_no=1
        atom_name='X'

        for res in array:
            for idx, atom_coord in enumerate(res):
                serial=idx+1
                atom=[atom_name+str(serial), atom_coord]
                atoms.append((model_id, serial, atom, residue+str(residue_no), chain))
            residue_no+=1
        # for idx, atom_coord in enumerate(array[0]): #this takes into consideration that it's of dimensions (1, n, 3)
        #     serial=idx+1
        #     atom=[atom_name+str(serial), atom_coord]
        #     atoms.append((model_id, serial, atom, residue, chain))

        return atoms

    # -- xml processing
    def flattenMolecule_to_dict(self,rna_molecule:RNA_Molecule):
        '''
        rna_molecule: RNA_Molecule object -> RNA molecule to be flattened -> list of atom dictionaries
        '''
        atoms_list = []

        for model_num,_ in enumerate(rna_molecule.get_models()):  #--looping through all models 
            model=rna_molecule.get_models()[_] # --model object from dict key
            
            for chain in model.get_chains().values(): #--looping through all chains
                for residue in chain.get_residues().values(): #--looping through all residues  
                    for atom_key, atom in residue.get_atoms().items(): #--looping through all atoms
                        atom_id, alt_id = atom_key  # unpacking atom key (alt_id is '' if no alt location)
                        # --keys defined identically to pdbml format, values extracted directly from atom object
                        atom_data = {
                            "atom_id": str(len(atoms_list) + 1),  # Assign a sequential ID
                            "B": str(atom.temp_factor),
                            "x": str(atom.x),
                            "y": str(atom.y),
                            "z": str(atom.z),
                            "chain_id": chain.id,
                            "atom_id": atom_id,
                            "residue_type": residue.type.name,
                            "residue_pos": str(residue.position),
                            "alt_id": None if alt_id == "" else alt_id,
                            "occupancy": str(atom.occupancy),
                            "model_no": model_num+1,
                            "atom_element": atom.element.name
                        }
                        atoms_list.append(atom_data)
        return atoms_list