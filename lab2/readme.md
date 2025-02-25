# Lab 2 Report

## Table of contents

- [Lab 2 Report](#lab-2-report)
  - [Table of contents](#table-of-contents)
  - [Demo](#demo)
  - [Class Diagram](#class-diagram)
  - [Object Diagram](#object-diagram)
  - [Implementation](#implementation)
  - [Extensions](#extensions)



Demo test on python notebook (can't host private repo code on google colab, sofor now cn only ik it to the `.ipynb` file): 

Demo directory:

```text
lab2/
└── demo
   ├── demo.ipynb              # main demo demonstrating reading and writing
   └── demo-extensions.ipynb   # demo for extension features
```

[![Demo](https://img.shields.io/badge/main_demo-notebook-orange)](./demo/demo.ipynb)  [![Demo2](https://img.shields.io/badge/extension_demo-notebook-orange)](./demo/demo-extensions.ipynb)


## Class Diagram

<p align='center'>
<img src='./model/Class-Diagram.jpg' alt='class diagram'>
<figcaption align='center'>Class Diagram</figcaption>
</p>

As a minor enhancement to the previous lab design, we added `Species` entity to represent a class Species that is associated with `RNA_Molecule`. Instead of using attribute `species` in `RNA_Molecule` class as string type, it is now of `Species` type. An `RNA_Molecule` can have 1 `Species` or none (e.g., if it is synthetic). A `Species` can have many `RNA_Molecule` instances.

For the purpose of this lab (reading/writing to a file), new classes have been introduced in yellow in this diagram: 

1. `RNA_IO` **(User Interface for I/O Operations)**
    - Serves as the interface for reading and writing RNA sequence files.
    - Provides two methods:
        - `read(path, format, coarse_grained=False, atom_name=None)` → `RNA_Molecule`
            - Parses a file and returns an RNA_Molecule instance.
            - Optional parameters:
                - `coarse_grained`: If True, extracts only a subset of atoms for a simplified representation.
                - `atom_name`: Allows specifying a particular atom type to extract.
        - `write(rna_molecule, file_path, format)`
            - Writes an `RNA_Molecule` instance to a file.
    - Handles multiple file formats by relying on specialized `parsers` and `writers` for format-specific processing → can have many parsers and writers.

2. **Parsing** 
    - `RNA_Parser` (Abstract Class)
        - Defines the abstract method `read()`, enforcing child classes to implement format-specific parsing.
    - `PDB_Parser` (Concrete Class)
        - Implements `read()`, processing PDB files to create an RNA_Molecule instance.
  
3. **Writing**
    -  `RNA_Writer` (Abstract Class)
       - Defines the abstract method `write()`, ensuring all writers implement format-specific writing.
    - `PDB_Writer` (Concrete Class)
        - Implements `write()`, converting an RNA_Molecule instance into a PDB file.

4. `Processor` **(RNA Structure Representation Handler)**
    - An intermediary between parsers/writers and RNA_Molecule.
    - Converts parsed content into an RNA_Molecule instance.
    - Flattens an RNA_Molecule into a list of atoms for writing.
    - Associations:
        - `PDB_Parser` uses a `Processor` to construct `RNA_Molecule`.
        - `PDB_Writer` uses a `Processor` to extract relevant data for writing.
        - An `RNA_Molecule` can be associated with multiple `Processor` instances.
        - A `Processor` can belong to at most one `parser` or one `writer` (0..1 relationship). 

5. **Design Choice**
    - Decoupling:
        - RNA_IO provides a simple interface for users.
        - Parsers and Writers handle format-specific operations.
        - Processor ensures proper RNA representation.
    - Extensibility:
        - New formats (e.g., FASTA) can be supported by adding corresponding RNA_Parser and RNA_Writer subclasses.



## Object Diagram

<p align='center'>
<img src='./model/Object-Diagram.jpg' alt='object diagram'>
<figcaption align='center'>Object Diagram</figcaption>
</p>

## Implementation


## Extensions

_Some enhancements on the library design that are worth of mention:_

### Directory Structure

In lab1, we had a flat directory structure. In lab2, we have introduced a new directory structure to better organize the code into modules and submodules. The new structure is as follows:

```text
src/
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
│   └── writers
│       ├── PDB_Writer.py
│       ├── RNA_Writer.py
│       └── __init__.py
├── Structure
│   ├── Atom.py
│   ├── Chain.py
│   ├── Model.py
│   ├── RNA_Molecule.py
│   ├── Residue.py
│   └── __init__.py 
├── processor.py
└── utils.py
```

The interdependencies between modules have been handled by appending the `src` directory to the pythonpath and importing the modules using absolute imports. Another alternative during the development stage (not a deployable library yet) is tu sue the [`set-pythonpath.sh`](../dev/set-pythonpath.sh) script in `dev/` directory.

### Handling 1-N Relationships

Originally, if we have a 1-N relationship between two classes, _e.g., one Family have many RNA Molecules_, we would store a list of RNA Molecules in the Family class. This is a simple and straightforward approach. However, it has some drawbacks, as it makes us unable to tag each RNA Molecule with the Family it belongs to. To address this issue, we have added an attribute "family" to the RNA Molecule class, that the user has no interaction whatsoever with, but is rather set automatically through the code when the RNA Molecule is added to a Family. 

> [!CAUTION]
To ensure this behavior we have either not provided a setter for this attribute or raised a warning message if the user tries to set it manually. A private method has been implemented that acts as a setter for this attribute in the other class (_e.g., RNA_Molecule's `_add_family()` method will be used in Family's add_RNA() method through: `fam1.add_RNA(rna1)`; behind the scenes: `rna1._add_family(self)  `_).

This was done in all classes that have a 1-N relationship with another class.