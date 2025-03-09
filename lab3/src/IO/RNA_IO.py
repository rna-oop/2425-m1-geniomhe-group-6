'''
RNA_IO module contains class RNA_IO for input/output operations
'''
import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from IO.parsers.PDB_Parser import PDB_Parser
from IO.writers.PDB_Writer import PDB_Writer
from IO.writers.PDBML_Writer import PDBML_Writer

class RNA_IO:
    
    def __init__(self):
        self.__parsers={"PDB": PDB_Parser()}
        self.__writers={"PDB": PDB_Writer(),'PDBML': PDBML_Writer(),'XML': PDBML_Writer()}
    
    def read(self, path_to_file, format, coarse_grained=False, atom_name="C1'", array=True):
        """
        Reads a PDB file and returns the RNA molecule object.
        """
        if format not in self.__parsers:
            raise ValueError(f"Format {format} is not supported")
        parser=self.__parsers[format]
        return parser.read(path_to_file, coarse_grained, atom_name, array)
    
    def write(self, rna_molecule, path_to_file, format):
        """
        Writes the RNA molecule object to a PDB file.
        """
        if format not in self.__writers:
            raise ValueError(f"Format {format} is not supported")
        writer=self.__writers[format]
        writer.write(rna_molecule, path_to_file)
    
#Example Usage

from utils import pathify_pdb

if __name__ == "__main__":
    rna_io=RNA_IO()

    pdb_path_test=pathify_pdb("7eaf")

    mol=rna_io.read(pdb_path_test, "PDB")
    
    print(mol)
    print(mol.shape)
    print(mol[0, -1, 0, :])
    
    """
    rna_io.write(mol, "1r7w_test.pdb", "PDB")
    
    mol1=rna_io.read(pdb_path_test, "PDB")
    
    print(mol)
    import numpy as np
    print(np.shape(mol1))
    print(mol1[0, -1, 0, :])
    
    """