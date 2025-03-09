'''
PDBML_Write module contains the class PDB_Writer which is responsible for writing the RNA molecule to a PDBML/XML file
'''

from typing import Union
import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from IO.writers.RNA_Writer import RNA_Writer
from Structure.RNA_Molecule import RNA_Molecule
from processor import Processor

import numpy as np

import xml.etree.ElementTree as ET

# -- helpers (maybe add to util since related to formatting files)
def wrap_str_to_xml(s,name='pdbml_output.xml'):
    with open(name, "w") as f:
        f.write(s)

class PDBML_Writer(RNA_Writer):
    
    def write(self, rna_molecule: Union[RNA_Molecule, np.ndarray], path_to_file):
        '''
        writes the RNA molecule object to a PDBML/XML file
        '''
        if (not isinstance(rna_molecule, RNA_Molecule)) and (type(rna_molecule) is not np.ndarray):
            raise TypeError(f"Expected an RNA_Molecule object or a numpy array, got {type(rna_molecule)}")

        processor=Processor()

        if isinstance(rna_molecule, RNA_Molecule):
            xml_str=processor.create_xml_from_molecule(rna_molecule)
            wrap_str_to_xml(xml_str, path_to_file)

        print(f"RNA molecule written to {path_to_file}")



