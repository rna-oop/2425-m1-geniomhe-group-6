'''
--- visitor submodule ---
contains the implementation of:
> Visitor interface (abstract class)
> XMLExportVisitor class implements Visitor interface (inherits from abstract class)
> PDBExportVisitor class implements Visitor interface (inherits from abstract class)

since in python there is no direct method 
'''

import os,sys
# sys.path.append(os.path.abspath('lab3/src'))

from RNAr.Structure.RNA_Molecule import RNA_Molecule

from abc import ABC, abstractmethod


class Visitor(ABC):
    '''
    abstract class defined in order to build the _Visitor_ design pattern
    >meant to be inherted by *XMLExportVisitor* and *PDBExportVisitor* classes 
    >contains abstract methods to be implemented by the child classes:
        - export
        - visit_RNA_Molecule
        - visit_Model
        - visit_Chain
        - visit_Residue
        - visit_Atom
    '''

    @abstractmethod
    def export(self, rna_molecule:RNA_Molecule, path):
        '''
        method to export the RNA_Molecule object to a file
        '''
        pass

    @abstractmethod
    def visit_RNA_Molecule(self, rna:RNA_Molecule):
        '''
        method to format the RNA_Molecule attributes to a string 
        it will be implemented differently in each child class
        '''
        pass

    @abstractmethod
    def visit_Model(self, model):
        pass
    
    @abstractmethod
    def visit_Chain(self, chain):
        pass
    
    @abstractmethod
    def visit_Residue(self, residue):
        pass
    
    @abstractmethod
    def visit_Atom(self, atom):
        pass