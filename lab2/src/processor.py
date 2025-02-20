from Structure.RNA_Molecule import RNA_Molecule, Model, Chain, Residue, Atom

class Processor:
    
    def __init__(self):
        self.entry_id = None
        experiment = None
        species = None
        rna_molecule= None
        self.atoms=[]
        
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
            model=Model(model_id)
            chain=Chain(chain_id)
            residue=Residue(residue_name, residue_id)
            atom=Atom(atom_name, x, y, z, element)
            residue.add_atom(atom)
            chain.add_residue(residue)
            model.add_chain(chain)
            self.rna_molecule.add_model(model)
        return self.rna_molecule
        
