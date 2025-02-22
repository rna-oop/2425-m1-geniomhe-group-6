'''
module RNA_Molecule contains class RNA_Molecule
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from Structure.Model import Model
from Families.species import Species


class RNA_Molecule:
    
    def __init__(self, entry_id: str, experiment: str, species: Species, models=None):
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
        if not isinstance(experiment, str):
            raise TypeError(f"experiment must be a string, got {type(experiment)}")
        self._experiment=experiment
        
    @property
    def species(self):
        return self._species
    
    @species.setter
    def species(self, species):
        if not isinstance(species, Species):
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
    

    def print_all(self, output_dir="lab1/data"):
        """
        Prints all models available for this RNA molecule entry, along with the atoms in each model.
        The output is written to a PDB-like formatted file:
        ATOM <atom_number> <atom_name> <residue_type> <chain_id> <residue_position> <x> <y> <z> <element>

        Parameters:
        - output_dir (str): The directory where the output file will be saved.
        """
        os.makedirs(output_dir, exist_ok=True)  #Ensure the directory exists

        filename = os.path.join(output_dir, f"{self.entry_id}_output.pdb")

        with open(filename, "w") as file:  #Open file for writing
            file.write(str(self) + "\n")  #Save the RNA molecule information
            
            for model in self._models.values():
                file.write(str(model) + "\n")
                atom_number = 1
                for chain in model.get_chains().values():
                    for residue in chain.get_residues().values():
                        for atom in residue.get_atoms().values():
                            file.write(f"ATOM {atom_number} {atom.atom_name.value} {atom.altloc} {residue.type.value} {chain.id} {residue.position} {atom.x} {atom.y} {atom.z} {atom.occupancy} {atom.element.value}\n")
                            atom_number += 1

        #Print the contents of the saved file
        with open(filename, "r") as file:
            print(file.read())


        
#Example usage

if __name__ == "__main__":
    
    species = Species("Homo Sapiens")
    rna1 = RNA_Molecule("1A9N", "NMR", species)
    print(rna1) #Output 1A9N NMR Homo sapiens
    m1 = Model(1)
    m2 = Model(2)
    m3 = Model(3)
    rna1.add_model(m1)
    rna1.add_model(m2)
    rna1.add_model(m3)
    print(rna1.get_models()) #Output [Model 1, Model 2, Model 3]
    rna1.remove_model(m3) 
    print(rna1.get_models()) #Output [Model 1, Model 2]
    rna1.print_all() 
    #Output 1A9N NMR Homo sapiens
    #Model 1
    #Model 2

