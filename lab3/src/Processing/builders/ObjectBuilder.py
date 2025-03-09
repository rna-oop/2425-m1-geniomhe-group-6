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
        
    def reset(self):
        self.__molecule = RNA_Molecule("")
        
    @property
    def molecule(self):
        molecule = self.__molecule
        self.reset()
        return molecule
    
    def add_model(self, model_id):
        self.__molecule.add_model(Model(model_id))
        
    def add_chain(self, chain_id):
        self.__molecule.get_models()[-1].add_chain(Chain(chain_id)) 
        
    def add_residue(self, *residue_args):
        self.__molecule.get_models()[-1].get_chains()[-1].add_residue(Residue(*residue_args))
        
    def add_atom(self, *atom_args):
        self.__molecule.get_models()[-1].get_chains()[-1].get_residues()[-1].add_atom(Atom(*atom_args))
        
    def add_molecule_info(self, entry_id, experiment, species):
        self.__molecule.entry_id = entry_id
        self.__molecule.experiment = experiment
        if species is not None:
            self.__molecule.species = Species(species)
        else:
            self.__molecule.species = None
        