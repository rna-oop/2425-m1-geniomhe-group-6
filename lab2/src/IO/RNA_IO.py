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
rna_io=RNA_IO()
mol=rna_io.read("/mnt/c/Users/dell/OneDrive/Master/M1/Periode_3/OOP2/2425-m1-geniomhe-group-6/lab1/data/7eaf/7eaf.pdb", "PDB")
mol.print_all()