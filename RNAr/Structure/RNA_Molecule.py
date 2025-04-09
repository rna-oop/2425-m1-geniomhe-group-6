'''
--- RNA_Molecule submodule ---
contains the implementation of:
> Structure interface (abstract class)
> RNA_Molecule class implements Structure interface (inherits from abstract class)
'''

import os,sys
# sys.path.append(os.path.abspath('lab3/src'))

from RNAr.Structure.Structure import Structure
from RNAr.Structure.Model import Model
from RNAr.Families.species import Species

from abc import ABC, abstractmethod

# from Processing.visitors.visitor import Visitor as V #circular imports



class RNA_Molecule(Structure):
    
    def __init__(self, entry_id: str, experiment=None, species=None, models=None):
        self.entry_id = entry_id
        self.experiment = experiment
        self.species = species
        self._models = models if models is not None else {} 

        
    @property
    def entry_id(self):
        return self._entry_id
    
    @entry_id.setter
    def entry_id(self, entry_id):
        if not isinstance(entry_id, str):
            raise TypeError(f"entry_id must be a string, got {type(entry_id)}")
        self._entry_id=entry_id
    
    @property
    def experiment(self):
        return self._experiment
    
    @experiment.setter
    def experiment(self, experiment):
        if experiment is not None and not isinstance(experiment, str):
            raise TypeError(f"experiment must be a string, got {type(experiment)}")
        self._experiment=experiment
        
    @property
    def species(self):
        return self._species
    
    @species.setter
    def species(self, species):
        if isinstance(species,str):
            species = Species(species)
        if not isinstance(species, Species) and species is not None:
            raise TypeError(f"species must be a Species object, got {type(species)}; please provide the species name either in string or Species type")
        
        if species is not None:
            species._add_molecule(self)
            self._species=species
        else:
            self._species=None
        
    def add_model(self, model):
        if not isinstance(model, Model):
            raise TypeError(f"Expected a Model instance, got {type(model)}")
        if model.id not in self._models:
            self._models[model.id] = model
            model._add_rna_molecule(self)
        
    def get_models(self):
        return self._models  
    
    def remove_model(self, model):
        self._models.pop(model.id)
        
        
    def __repr__(self):
        return f"ID: {self.entry_id} Experiment: {self.experiment} {self.species}"

    def accept(self, visitor:'Visitor'):
        visitor.visit_RNA_Molecule(self)

        
#Example usage

if __name__ == "__main__":
    
    species = 'Homo Sapiens' #handles automatic conversion of string to type Species successfully (minimizing error and enhancing ui)
    rna1 = RNA_Molecule("1A9N", "NMR", species)
    print(rna1) #Output ID: 1A9N Experiment: NMR Species: Homo Sapiens
    m1 = Model(1)
    m2 = Model(2)
    m3 = Model(3)
    rna1.add_model(m1)
    rna1.add_model(m2)
    rna1.add_model(m3)
    print(rna1.get_models()) #Output {1: Model 1, 2: Model 2, 3: Model 3}
    rna1.remove_model(m3) 
    print(rna1.get_models()) #Output {1: Model 1, 2: Model 2}

    # -- testing creation of 2 species with same name
    rna2=RNA_Molecule('7tim','XRAY','Homo sapiens') 
    print(rna1.species.declared_species) # able to recognize both species entries as one: successful

    # -- testing the 1-N composition with Model
    m_test=Model(1)
    rna2.add_model(m_test)
    print(m_test.rna_molecule)
    #amazingness
