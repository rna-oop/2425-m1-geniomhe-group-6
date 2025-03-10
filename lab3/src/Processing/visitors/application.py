# -- necessary setup

import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from IO.RNA_IO import RNA_IO
from utils import pathify_pdb

from xml_visitor import XMLExportVisitor
from pdb_visitor import PDBExportVisitor

def main():
    #-- reading using builder
    rna_io=RNA_IO()
    pdb_path=pathify_pdb('7EAF')
    mol=rna_io.read(pdb_path, "PDB",array=False)
    v=PDBExportVisitor()
    mol.accept(v)
    # print(mol)

if __name__ == "__main__":
    main()
