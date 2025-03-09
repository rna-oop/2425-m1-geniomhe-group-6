'''
RNA writer module, contains abstract class RNA_Writer (interface) that is implemented by PDB_Writer and XML_Writer
'''

import os,sys
sys.path.append(os.path.abspath('lab3/src'))
from Structure.RNA_Molecule import RNA_Molecule

from abc import ABC, abstractmethod
from typing import Union
import numpy as np

class RNA_Writer(ABC):
    
    @abstractmethod
    def write(self, rna_molecule: Union[RNA_Molecule, np.ndarray], path_to_file:str):
        '''
        this abstract method is enforced by all classes that inherit from RNA_Writer

        *can not check for input type from this method since it's abstract, but it's expected to get an RNA_Molecule object or a numpy array representing the RNA molecule, as per the header description*

        it takes as parameters:
        - rna_molecule: an RNA_Molecule object or a numpy array representing the RNA molecule
        - path_to_file: the path to the file where the RNA molecule will be written
        '''
        pass