'''
--- visitor submodule ---
contains the implementation of:
> Visitor interface (abstract class)
> XMLExportVisitor class implements Visitor interface (inherits from abstract class)
> PDBExportVisitor class implements Visitor interface (inherits from abstract class)

since in python there is no direct method 
'''

import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from Structure.RNA_Molecule import RNA_Molecule

from abc import ABC, abstractmethod


class Visitor(ABC):
    '''
    abstract class defined in order to build the _Visitor_ design pattern
    >meant to be inherted by *XMLExportVisitor* and *PDBExportVisitor* classes and enforces the implementation of the *visit* method

    - abstract methods:
        visit_RNA_Molecule(rna:RNA_Molecule) -> None

    *since there is no other concrete components*

    '''


    @abstractmethod
    def visit_RNA_Molecule(self, rna:RNA_Molecule):
        '''
        abstract method that is meant to be implemented by the classes that inherit from Visitor;  
        allows the visitor to visit the class that implements this method
        '''
        pass
