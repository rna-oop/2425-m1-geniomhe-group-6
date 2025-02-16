from RNA_Molecule import RNA_Molecule
from Model import Model
from Chain import Chain
from Residue import Residue
from Atom import Atom


#Creating an RNA molecule
rna_molecule = RNA_Molecule("1JAT", "X-RAY DIFFRACTION", "Homo sapiens")

#Creating a model
model1 = Model(1)

#Creating a chain
ch1 = Chain('A')

#Adding the model to the RNA molecule
rna_molecule.add_model(model1)

#Adding the chain to the model
model1.add_chain(ch1)

#Creating Residues
res1=Residue("A", 1)
res2=Residue("U", 2)
res3=Residue("C",3)

#Adding Residues
ch1.add_residue(res1)
ch1.add_residue(res2)
ch1.add_residue(res3)

#Creating Atoms
a1=Atom("OP1", 0.1, 0.2, 0.3, "O")
a2=Atom("P", 0.4, -0.5, 0.6, "P")
a3=Atom("N1", 0.25, 0.54, 0.23, "N")
a4=Atom("C4", 0.21, 0.76, -0.93, "C")

#Adding Atoms
res1.add_atom(a1)
res2.add_atom(a2)
res3.add_atom(a4)
res3.add_atom(a3)


print(rna_molecule.get_models())
print(rna_molecule.get_models()[0].get_chains())
print(rna_molecule.get_models()[0].get_chains()[0].get_residues())
print(rna_molecule.get_models()[0].get_chains()[0].get_residues()[0].get_atoms())

#Print the structure
rna_molecule.print_all()