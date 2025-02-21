'''
PDB_Write module contains the class PDB_Writer which is responsible for writing the RNA molecule to a PDB file
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from RNA_Writer import RNA_Writer

class PDB_Writer(RNA_Writer):
    
    def write(self, rna_molecule, path_to_file):
        pass
