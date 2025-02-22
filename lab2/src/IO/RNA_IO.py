'''
RNA_IO module contains class RNA_IO for input/output operations
'''
import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from IO.parsers.PDB_Parser import PDB_Parser
from IO.writers.PDB_Writer import PDB_Writer

class RNA_IO:
    
    def __init__(self):
        self.parsers={"PDB": PDB_Parser()}
        self.writers={"PDB": PDB_Writer()}
    
    def read(self, path_to_file, format):
        """
        Reads a PDB file and returns the RNA molecule object.
        """
        if format not in self.parsers:
            raise ValueError(f"Format {format} is not supported")
        parser=self.parsers[format]
        return parser.read(path_to_file)
    
    def write(self, rna_molecule, path_to_file, format):
        """
        Writes the RNA molecule object to a PDB file.
        """
        if format not in self.writers:
            raise ValueError(f"Format {format} is not supported")
        writer=self.writers[format]
        writer.write(rna_molecule, path_to_file)
    
#Example Usage

from utils import pathify_pdb

if __name__ == "__main__":
    rna_io=RNA_IO()

    pdb_path_test=pathify_pdb("7eaf")

    mol=rna_io.read(pdb_path_test, "PDB")
    rna_io.write(mol, "7eaf_test.pdb", "PDB")
    
    mol1=rna_io.read("7eaf_test.pdb", "PDB")
    rna_io.write(mol1, "7eaf_test1.pdb", "PDB")
    
    
