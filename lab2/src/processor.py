'''
module processor contains class Processor for handling parse/write operations (helper)
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from Structure.RNA_Molecule import RNA_Molecule
from Structure.Model import Model
from Structure.Chain import Chain
from Structure.Residue import Residue
from Structure.Atom import Atom
from Families.species import Species

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
        
        self.rna_molecule = RNA_Molecule(self.entry_id, self.experiment, self.species)
        
        for atom in self.atoms:
            
            atom_name, x, y, z, element, residue_name, residue_id, chain_id, altloc, occupancy, temp_factor, i_code, charge, model_id = atom
            
            self.rna_molecule.add_model(Model(model_id))
            model = self.rna_molecule.get_models()[model_id]
            model.add_chain(Chain(chain_id))
            chain = model.get_chains()[chain_id]
            chain.add_residue(Residue(residue_name, residue_id))
            residue = chain.get_residues()[residue_id]
            residue.add_atom(Atom(atom_name, x, y, z, element, altloc, occupancy, temp_factor, i_code, charge))
                
        return self.rna_molecule

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


