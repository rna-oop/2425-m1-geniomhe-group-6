from Model import Model

class RNA_Molecule:
    
    def __init__(self, entry_id: str, experiment: str, species: str):
        self.entry_id = entry_id
        self.experiment = experiment
        self.species = species
        self._models = []
        
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
        if not isinstance(species, str):
            raise TypeError(f"species must be a string, got {type(species)}")
        self._species=species
        
    def add_model(self, model):
        self._models.append(model)
        
    def get_models(self):
        return self._models  
    
    def remove_model(self, model):
        self._models.remove(model)
        
        
    def __repr__(self):
        return f"{self.entry_id} {self.experiment} {self.species}"
    
    def print_all(self):
        """
        A function to print all the models available for this RNA molecule entry, along with the atoms in each model.
        For each Model, it prints on a new line the information with the following format similar to pdb format:
        ATOM <atom_number> <atom_name> <residue_type> <chain_id> <residue_position> <x> <y> <z> <element>
        """
        print(self)
        for model in self._models:
            print(model)
            atom_number=1
            for chain in model.get_chains():
                for residue in chain.get_residues():
                    for atom in residue.get_atoms():
                        print(f"ATOM {atom_number} {atom.atom_name} {residue.type.value} {chain.id} {residue.position} {atom.x} {atom.y} {atom.z} {atom.element} \n")
                        atom_number+=1
        
#Example usage
'''
rna1 = RNA_Molecule("1A9N", "NMR", "Homo sapiens")
print(rna1)
m1 = Model(1)
m2 = Model(2)
m3 = Model(3)
rna1.add_model(m1)
rna1.add_model(m2)
rna1.add_model(m3)
print(rna1.get_models())
rna1.remove_model(m3)
print(rna1.get_models())
rna1.print_all()
'''