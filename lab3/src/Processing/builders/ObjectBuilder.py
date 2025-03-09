import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from Structure.RNA_Molecule import RNA_Molecule
from Structure.Model import Model
from Structure.Chain import Chain
from Structure.Residue import Residue
from Structure.Atom import Atom
from Families.species import Species
from Processing.builders.Builder import Builder
class ObjectBuilder(Builder):
    """
    The ObjectBuilder class is responsible for constructing the RNA molecule object.
    """
    def __init__(self):
        self.reset()
        self.__model_id = 0
        self.__chain_id = 0
        self.__residue_id = 0
        
    def reset(self):
        self.__molecule = RNA_Molecule("")
        
    @property
    def molecule(self):
        molecule = self.__molecule
        self.reset()
        return molecule
    
    def add_model(self, model_id):
        self.__molecule.add_model(Model(model_id))
        self.__model_id = model_id 
        
    def add_chain(self, chain_id):
        self.__molecule.get_models()[self.__model_id].add_chain(Chain(chain_id)) 
        self.__chain_id = chain_id
        
    def add_residue(self, *residue_args):
        self.__molecule.get_models()[self.__model_id].get_chains()[self.__chain_id].add_residue(Residue(*residue_args))
        self.__residue_id = residue_args[1]
        
    def add_atom(self, *atom_args):
        self.__molecule.get_models()[self.__model_id].get_chains()[self.__chain_id].get_residues()[self.__residue_id].add_atom(Atom(*atom_args))
        
    def add_molecule_info(self, entry_id, experiment, species):
        self.__molecule.entry_id = entry_id
        self.__molecule.experiment = experiment
        if species is not None:
            self.__molecule.species = Species(species)
        else:
            self.__molecule.species = None
        