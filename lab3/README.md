# Lab 3 Report

## Table of contents

- [Lab 3 Report](#lab-3-report)
  - [Table of contents](#table-of-contents)
  - [First Implementation](#first-implementation)
    - [Class Diagram for the Previous-Model-Extension](#class-diagram-for-the-previous-model-extension)
    - [Object Diagram for the Previous-Model-Extension](#object-diagram-for-the-previous-model-extension)
    - [1. Parser returns a numpy array](#1-parser-returns-a-numpy-array)
  - [Main Implementation using Design Patterns](#main-implementation-using-design-patterns)
    - [Class Diagram](#class-diagram)
    - [Object Diagram](#object-diagram)
    - [1. Builder Design Pattern](#1-builder-design-pattern)
    - [2. Visitor Design Pattern](#2-visitor-design-pattern)
  - [Advantages and Disadvantages](#advantages-and-disadvantages)

## First Implementation

**This implementation is in the branch `previous-model-extension `.**

In this lab, we extended our previous model to include the following functionalities:
- The parser returns a numpy array representation of the molecule.
- Writing structures into PDML/XML format.

First, we kept our previous model and extended it with the minimal changes possible without using the design patterns. 

### Class Diagram for the Previous-Model-Extension 

![Class-Diagram](model/Class-Diagram-Previous.jpg)

The new changes are highlighted in white.

### Object Diagram for the Previous-Model-Extension

![Object-Diagram](model/Object-Diagram-Previous.jpg)

### 1. Parser returns a numpy array

For this, we added a function in the `Processor` class called: `createArray()` that returns the required numpy array representation of an `RNA Molecule` that can have multiple models. 

Note: In our previous implementation, the parser will store the atom information in a list `atoms` inside the `Processor` class.

**createArray()** in `Processor` class:
- Returns a numpy array representation of the molecule
- Dimension: `(number of models, max_residues_no, max_atoms_per_residue_no, 3)` 
- Stores the x,y,z coordinates of each atom.
- Implementation notes:
  - To find the number of models we checked the model_id of the last atom in the atoms list. 
  - We had to loop through the list of atoms to find the maximum number of residues among all models and the maximum number of atoms per residue.
  - Considering that the same atom in a residue can have different coordinates (alternate locations), we stored the coordinates of the atom that has the highest occupancy.
  - The array is filled with nan values where there is no atom information.

**read() in `PDB_Parser` class:**
We added a boolean argument `array` to the `read()` function and set it to `True` by default. If the argument is `True`, the function will return the numpy array representation of the molecule, otherwise it will create the molecule object as before. We did not change anything in the `read()` function, we just added the following at the end:

```python
if array:
    return processor.createArray()
else:         
    return processor.createMolecule() 
```

**Code Usage**
An example can be found in the notebook [reading.ipynb](./demo/reading.ipynb). 
We read a molecule that contains 1 model and another molecule that contains multiple models, and showed the resulting arrays. 
A brief example:

```python
rna_io=RNA_IO()

pdb_path_test=pathify_pdb("7eaf")

mol=rna_io.read(pdb_path_test, "PDB")

print(mol.shape)
print(mol[0, -1, 0, :])
```

The output: 
```
(1, 94, 24, 3)
[-10.06    7.177 -49.234]
```

## Main Implementation using Design Patterns

### Class Diagram


### Object Diagram


### 1. Builder Design Pattern


### 2. Visitor Design Pattern


## Advantages and Disadvantages




































































