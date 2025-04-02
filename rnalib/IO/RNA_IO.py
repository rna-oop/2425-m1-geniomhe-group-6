'''
RNA_IO module contains class RNA_IO for input/output operations
'''
import os,sys
sys.path.append(os.path.abspath('lab4/src'))

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
    
    
    def parse_pdb_files(entries: list):
        """
        Parses a list of PDB entries and returns a numpy array of stacked molecules.
        Dimension: (number of files including different models, number of residues, number of atoms, 3)
        """
        rna_io = RNA_IO()
        all_molecules = []

        for entry in entries:
            pdb_path_test = fetch_pdb_file(entry)
            mol_array = rna_io.read(pdb_path_test, "PDB")
            all_molecules.append(mol_array)

        max_residues = max(mol.shape[1] for mol in all_molecules)
        max_atoms = max(mol.shape[2] for mol in all_molecules)

        padded_molecules = []
        
        for mol in all_molecules:
            padded = np.full((mol.shape[0], max_residues, max_atoms, 3), np.nan)
            padded[:, :mol.shape[1], :mol.shape[2], :] = mol
            padded_molecules.append(padded)

        stacked_molecules = np.vstack(padded_molecules)
        
        return stacked_molecules
    
    
#Example Usage

from utils import fetch_pdb_file

if __name__ == "__main__":
    
    rna_io=RNA_IO()

    pdb_path_test=fetch_pdb_file("1r7w")

    mol=rna_io.read(pdb_path_test, "PDB", array=False)
    
    rna_io.write(mol, "1r7w_test.pdb", "PDB")
    
    array, seq =rna_io.read(pdb_path_test, "PDB")
    
    print(array)
    import numpy as np
    print(np.shape(array))
    print(array[0, -1, 0, :])
    print(type(array))
    
    print(seq)
    print(np.shape(seq))
