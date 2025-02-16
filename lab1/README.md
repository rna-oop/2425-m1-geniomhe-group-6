# Lab 1 Report

## Class Diagram

![Class Diagram](/lab1/model/Class-Diagram.jpg)

According to this lab description, the first part is about RNA sequences and their spatial conformations. From the details and examples provided, we assumed that the RNA sequence that we want to model has a structure and the purpose is the manipulation of this structure. 

#### Entity Atom 
- Attributes: atom_name: AtomName, x: float, y: float, z: float, element: Element
- AtomName is an enumaration that contains all the possible atom names as present in pdb. 
- Element is an enumeration that contains all the possible atoms that can be present in an RNA nucleotide "C, O, P, N". 
- x y z are the coordinates of the atom in the 3D space.

#### Entity Residue
- Attributes: type: NBase, position: int
- NBase is an enumaration that contains all the possible residue types for RNA nucleotides "A, U, G, C".
- position is the position of the residue in the RNA sequence.
- There is a composition relationship between Residue and Atom. 1 Residue is composed of multiple atoms. If a Residue is deleted, all the atoms that are part of that residue will be deleted as well.


#### Entity Chain
- Attributes: id: str
- id is the identifier of the chain.
- There is a composition relationship between Chain and Residue. 1 Chain is composed of multiple residues (2 residues at least since a residue is a nucleotide that is linked by a phosphodiester bond to another nucleotide, even though of course it will be formed of many more residues). If a Chain is deleted, all the residues that are part of that chain will be deleted as well.

#### Entity Model
- Attributes: id: int
- id is the identifier of the model.
- We considered a model as a specific conformation of an RNA molecule (or structure). 
- There is a composition relationship between Model and Chain. 1 Model is composed of at least one chain. If a Model is deleted, all the chains that are part of that model will be deleted as well.

#### Entity RNA_Molecule
- Attributes: entry_id: int, experiment: str, species: str
- Since we considered that we are modeling only RNA molecules that have experimental structures, we defined attributes entry_id as in pdb entry id, experiment as the experiment that was performed to obtain the structure and species as the species source of where this RNA molecule was obtained from.
- An RNA_Molecule can have 1 or multiple models. If it was determined by X-Ray it will generally have only one model, but if it was determined by NMR it will have multiple models. And so for example if this RNA_Molecule was determined by NMR, we can access all the models that were generated from this NMR experiment, each model indexed by a number.

#### Entity Family
- Attributes: name: str, id: str, type: str 
- There exist an aggregation relationship between Family and RNA_Molecule. 1 Family consists of evolutionary related RNA sequences sharing common similarities. So a family should at least contain 2 RNA molecules that are similar. But there might exist an RNA molecule that is not part of any family maybe because it is unique or because it is not yet classified. It is aggregation relationship because we can assume that if a family is deleted the RNA molecules will still exist. 

#### Entity Clan
- Attributes: name: str, id: str
- Same logic as Family, but a Clan is a group of families that share common characteristics. So it will be an aggregation relationship and 1 clan consists of at least 2 families. But a family can exist without being part of any clan. 

#### Entity PhyloTree
- Since a phylogenetic tree here is defined for a given RNA family, hence a tree belongs only to one family. 
- But a family can have 0 (if it does not yet have a tree associated with it) or multiple phylogenetic trees (because probably different algorithms can be used to construct the tree, or different versions at different times can exist). 

#### Entity TreeNode




#### Species
It is described that species refer to the organisms that contain RNA sequences belonging to a particular RNA family. So a family can be distributed across multiple species, and a species can contain multiple families. But we did not include it as a separate class but rather as an attribute of RNA_Molecule, and so we can obtain the distribution of the species for a particular family by looking at the species attribute of the RNA_Molecules that are part of that family. And in this way, the species description can also be used in the phylogenetic tree. 



