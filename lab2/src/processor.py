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

class Processor:
    
    def __init__(self):
        self.entry_id = None
        self.experiment = None
        self.species = None
        self.rna_molecule = None
        self.atoms = []
        
        # Lookup dictionaries for tracking existing objects
        self.models = {}   # key: model_id, value: Model object
        self.chains = {}   # key: (model_id, chain_id), value: Chain object
        self.residues = {} # key: (model_id, chain_id, residue_id), value: Residue object
        
    def rna_info(self, entry_id, experiment, species):
        self.entry_id = entry_id
        self.experiment = experiment
        self.species = species
        
    def atom_info(self, *args):
        self.atoms.append(list(args))
        
    def createMolecule(self):
        
        self.rna_molecule = RNA_Molecule(self.entry_id, self.experiment, self.species)
        
        for atom in self.atoms:
            
            atom_name, x, y, z, element, residue_name, residue_id, chain_id, model_id = atom
            
            #Retrieve or create the model
            if model_id not in self.models:
                self.models[model_id] = Model(model_id)
            model = self.models[model_id]
            self.rna_molecule.add_model(model) #Add model to the RNA molecule
            
            #Retrieve or create the chain
            if (model_id, chain_id) not in self.chains:
                self.chains[(model_id, chain_id)] = Chain(chain_id)
            chain = self.chains[(model_id, chain_id)]
            model.add_chain(chain) #Add chain to the model
            
            #Retrieve or create the residue
            if (model_id, chain_id, residue_id) not in self.residues:
                self.residues[(model_id, chain_id, residue_id)] = Residue(residue_name, residue_id)
            residue = self.residues[(model_id, chain_id, residue_id)]
            print("Test", self.rna_molecule.get_models()[-1].get_chains())
            chain.add_residue(residue) #Add residue to the chain
            
            #Create the atom and add it to the residue
            atom = Atom(atom_name, x, y, z, element)
            residue.add_atom(atom) #Add atom to the residue
                
        return self.rna_molecule
