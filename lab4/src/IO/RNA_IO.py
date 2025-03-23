'''
RNA_IO module contains class RNA_IO for input/output operations
'''
import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from IO.parsers.PDB_Parser import PDB_Parser
from IO.visitor_writers.pdb_visitor import PDBExportVisitor
from IO.visitor_writers.xml_visitor import XMLExportVisitor
from Structure.RNA_Molecule import RNA_Molecule

class RNA_IO:
    
    def __init__(self):
        self.__parsers={"PDB": PDB_Parser()}
        self.__writers={"PDB": PDBExportVisitor(), "XML": XMLExportVisitor(), "PDBML": XMLExportVisitor()}
    
    def read(self, path_to_file, format, coarse_grained=False, atom_name="C1'", array=True):
        """
        Reads a file of specific format and returns a numpy array if array is True, else returns a RNA molecule object.
        """
        if format not in self.__parsers:
            raise ValueError(f"Format {format} is not supported")
        parser=self.__parsers[format]
        return parser.read(path_to_file, coarse_grained, atom_name, array)
    
    def write(self, rna_molecule: RNA_Molecule, path, format): 
        """
        Writes an RNA_Molecule object to a file of specific format.
        """
        if format not in self.__writers:
            raise ValueError(f"Format {format} is not supported")
        exporter=self.__writers[format]
        if not isinstance(rna_molecule, RNA_Molecule):
            raise ValueError("RNA_Molecule object expected")
        exporter.export(rna_molecule, path)
    
#Example Usage

from utils import pathify_pdb

if __name__ == "__main__":
    rna_io=RNA_IO()

    pdb_path_test=pathify_pdb("1r7w")

    mol=rna_io.read(pdb_path_test, "PDB", array=False)
    
    rna_io.write(mol, "1r7w_test.pdb", "PDB")
    
    mol1=rna_io.read(pdb_path_test, "PDB")
    
    print(mol1)
    import numpy as np
    print(np.shape(mol1))
    print(mol1[0, -1, 0, :])
    print(type(mol1))
    
