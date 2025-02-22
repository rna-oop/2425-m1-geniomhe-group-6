'''
module RNA_Molecule contains class RNA_Molecule
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from Structure.Model import Model
from Families.species import Species


class RNA_Molecule:
    
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
        if species is not None and not isinstance(species, Species):
            raise TypeError(f"species must be a Species object, got {type(species)}")
        self._species=species
        
    def add_model(self, model):
        if not isinstance(model, Model):
            raise TypeError(f"Expected a Model instance, got {type(model)}")
        if model.id not in self._models:
            self._models[model.id] = model
            model.rna_molecule = self
        
    def get_models(self):
        return self._models  
    
    def remove_model(self, model):
        self._models.pop(model.id)
        
        
    def __repr__(self):
        return f"ID: {self.entry_id} Experiment: {self.experiment} {self.species}"


        
#Example usage

if __name__ == "__main__":
    
    species = Species("Homo Sapiens")
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
