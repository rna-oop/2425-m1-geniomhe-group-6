# 2425-m1geniomhe-oop2-labs

* Joelle ASSY ([@JoelleAs](https://github.com/joelleas))
* Rayane ADAM ([@raysas](https://github.com/raysas))

## Modeling a Library for the Manipulation of Ribonucleic Acids (RNAs)
The goal of this series of labs is to build a library that allows easy manipulation and study of RNA sequences.

## Table of Contents
- [2425-m1geniomhe-oop2-labs](#2425-m1geniomhe-oop2-labs)
  - [Modeling a Library for the Manipulation of Ribonucleic Acids (RNAs)](#modeling-a-library-for-the-manipulation-of-ribonucleic-acids-rnas)
  - [Table of Contents](#table-of-contents)
  - [Labs](#labs)
    - [Lab1](#lab1)
    - [Lab2](#lab2)
    - [Lab3](#lab3)
    - [Lab4](#lab4)
  - [Overview of Library Functionalities](#overview-of-library-functionalities)
  - [Demo](#demo)
  - [Class Diagram](#class-diagram)
  - [Object Diagram](#object-diagram)
  - [Library Structure](#library-structure)
  - [Overview of Modules Implementation and Design Patterns](#overview-of-modules-implementation-and-design-patterns)
    - [Structure Module](#structure-module)
    - [Families Module](#families-module)
    - [IO Module](#io-module)
      - [Visitor Design Pattern](#visitor-design-pattern)
    - [Processing Module](#processing-module)
      - [Builder Design Pattern](#builder-design-pattern)
    - [Transformations Module](#transformations-module)
      - [Chain of Responsibility Design Pattern](#chain-of-responsibility-design-pattern)



## Labs
### Lab1
[description](lab1/lab1.pdf) | [report](lab1/README.md) | [contents](lab1/)

### Lab2
[description](lab1/lab2.pdf) | [report](lab2/README.md) | [contents](lab2/)

### Lab3
[description](lab1/lab3.pdf) | [report](lab3/README.md) | [contents](lab3/)

### Lab4
[description](lab1/lab4.pdf) | [report](lab4/README.md) | [contents](lab4/)




## Overview of Library Functionalities
The library is designed to manipulate and study RNA sequences. It provides functionalities for:
- Creating and manipulating RNA molecules objects.
- Reading PDB file and creating an RNA molecule object or a numpy array of coordinates. 
- Writing PDB and XML files from an RNA molecule object.
- Reading multiple PDB files into a single numpy array of sequences, and another numpy array of coordinates.
- Doing a Pipeline of Transformations on the sequences and coordinates arrays:
  - Normalize by cropping or padding the sequences.
  - Kmers
  - OneHotEncoding for a sequence or kmers 
  - Distograms, specific atoms can be given, and there is an option to bucketize the distances.
  - Secondary Structure prediction (dot-bracket notation) using Nussinov algorithm or Watson-Crick distances. 
  - Tertiaty Motifs detection (hairpins, internal loops, bulges) 

## Demo 

## Class Diagram
![Class Diagram](/model/class-diagram.jpg)
Each color represents a different module, and opacity variations indicate different submodules.

## Object Diagram
![Object Diagram](/model/object-diagram.jpg)

## Library Structure

The classes are organized in modules and submodules as follows:

```text
.
├── Families
│   ├── __init__.py
│   ├── clan.py
│   ├── family.py
│   ├── species.py
│   └── tree.py
├── IO
│   ├── RNA_IO.py
│   ├── __init__.py
│   ├── parsers
│   │   ├── PDB_Parser.py
│   │   ├── RNA_Parser.py
│   │   └── __init__.py
│   └── visitor_writers
│       ├── __init__.py
│       ├── pdb_visitor.py
│       ├── visitor.py
│       └── xml_visitor.py
├── Processing
│   ├── ArrayBuilder.py
│   ├── Builder.py
│   ├── Director.py
│   ├── ObjectBuilder.py
│   └── __init__.py
├── Structure
│   ├── Atom.py
│   ├── Chain.py
│   ├── Model.py
│   ├── RNA_Molecule.py
│   ├── Residue.py
│   ├── Structure.py
│   └── __init__.py
├── Transformations
│   ├── Pipeline.py
│   ├── __init__.py
│   └── transformers
│       ├── BaseTransformer.py
│       ├── Distogram.py
│       ├── Kmers.py
│       ├── Normalize.py
│       ├── OneHotEncoding.py
│       ├── SecondaryStructure.py
│       ├── TertiaryStructure.py
│       ├── Transformer.py
│       └── __init__.py
├── utils.py
└── viz.py
```

##  Overview of Modules Implementation and Design Patterns

### Structure Module

The `Structure` module is responsible for representing the RNA molecule and its components. It contains the hierarchical structure of the RNA molecule, including models, chains, residues, and atoms. The classes in this module are designed to work together to provide a comprehensive representation of the RNA structure.

**Structure class**:

An interface for all the classes in the Structure module. It enforces the implementation of the `accept` method, which is part of the Visitor design pattern that we will discuss later.

**Common Implementation**:

- Encapsulation and Validation: Attributes are accessed through `getters` and `setters`, ensuring data integrity and type validation.
- String Representation: The `__repr__` method provides a clear textual representation of objects.
- Hierarchical Data Storage:
  - Parent classes (RNA_Molecule, Model, Chain, Residue) store their children in `dictionaries`, enabling efficient access and manipulation.
  - Child classes (Atom, Residue, Chain, Model) maintain a `reference to their parent`, ensuring bidirectional navigation of the structure.
- Controlled Data Modification:
  - Parent classes have methods to `add`, `remove`, and `get` children while maintaining structural consistency.
  - Objects can be `initialized with existing children`, allowing flexible structure creation.
  
**Atom class**:
- Attributes: name, x, y, z, element, altloc=None, occupancy=None, temp_factor=None, charge=None
- Enum for the atom elements (C, N, O, P, H)

**Residue**:
- Attributes: type, position, i_code=None, atoms=None
- Enum for the residue types (A, C, G, U, X)

**Chain**:
- Attributes: id, residues=None

**Model**:
- It represents a model in the PDB file.
- A molecule can have multiple models (usually in NMR files).
- Attributes: id, chains=None

**RNA_Molecule**:
- It represents the entire RNA molecule.
- It contains multiple models, each with multiple chains.
- Attributes: entry_id, experiment=None, species=None, models=None

---

### Families Module

---

### IO Module

The `IO` module is responsible for reading and writing RNA structures from and to various file formats. It provides functionality to parse PDB files, create RNA molecule objects, and write RNA structures to PDB and XML files.

**RNA_IO class**:

- It serves as a user interface for reading and writing RNA structures from and to various file formats.
- It contains a dictionary of parsers and writers for different formats. 
- Currently, it supports `PDB` format for reading and PDB, `XML` or PDBML formats for writing.
- The `read` method reads a file of a specific format and returns either a numpy array or an RNA molecule object, depending on the `array` parameter.
- The `write` method writes an RNA molecule object to a file of a specific format.

**PDB_Parser class**:

#### Visitor Design Pattern


---

### Processing Module

#### Builder Design Pattern

---

### Transformations Module

#### Chain of Responsibility Design Pattern
