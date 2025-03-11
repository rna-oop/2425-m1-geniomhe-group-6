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

class PDBML_Writer(RNA_Writer):

    # -- helpers (maybe add to util since related to formatting files)
    def _wrap_str_to_xml(self,s,name='pdbml_output.xml'):
        with open(name, "w") as f:
            f.write(s)

    def _format_atom_info(self, atoms_list,entry_id):
        '''
        formats a list of atoms dicts into XML format
        '''
        s='''<?xml version="1.0" encoding="UTF-8" ?>
<PDBx:datablock datablockName="'''+entry_id+'''"
   xmlns:PDBx="http://pdbml.pdb.org/schema/pdbx-v50.xsd"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd">'''
        s+='\n\t<PDBx:atom_siteCategory>\n'
        for atom in atoms_list:
            s+='\t\t<PDBx:atom_site id="'+atom["atom_id"]+'">\n'
            s+='\t\t\t<PDBx:B_iso_or_equiv>'+str(atom['B'])+'</PDBx:B_iso_or_equiv>\n'
            s+='\t\t\t<PDBx:Cartn_x>'+str(atom['x'])+'</PDBx:Cartn_x>\n'
            s+='\t\t\t<PDBx:Cartn_y>'+str(atom['y'])+'</PDBx:Cartn_y>\n'
            s+='\t\t\t<PDBx:Cartn_z>'+str(atom['z'])+'</PDBx:Cartn_z>\n'
            s+='\t\t\t<PDBx:auth_asym_id>'+atom['chain_id']+'</PDBx:auth_asym_id>\n'
            s+='\t\t\t<PDBx:auth_atom_id>'+atom['atom_id']+'</PDBx:auth_atom_id>\n'
            s+='\t\t\t<PDBx:auth_comp_id>'+atom['residue_type']+'</PDBx:auth_comp_id>\n'
            s+='\t\t\t<PDBx:auth_seq_id>'+str(atom['residue_pos'])+'</PDBx:auth_seq_id>\n'
            s+='\t\t\t<PDBx:group_PDB>ATOM</PDBx:group_PDB>\n'
            if atom['alt_id'] is not None:
                s+='\t\t\t<PDBx:label_alt_id xsi:nil="true" />\n'
            else:
                atom['alt_id']='A'
            s+='\t\t\t<PDBx:label_asym_id>'+atom['alt_id']+'</PDBx:label_asym_id>\n'
            s+='\t\t\t<PDBx:label_atom_id>'+atom['atom_id']+'</PDBx:label_atom_id>\n'
            s+='\t\t\t<PDBx:label_comp_id>'+atom['residue_type']+'</PDBx:label_comp_id>\n'
            s+='\t\t\t<PDBx:label_entity_id>1</PDBx:label_entity_id>\n'
            s+='\t\t\t<PDBx:label_seq_id>'+str(atom['residue_pos'])+'</PDBx:label_seq_id>\n'
            s+='\t\t\t<PDBx:occupancy>'+str(atom['occupancy'])+'</PDBx:occupancy>\n'
            s+='\t\t\t<PDBx:pdbx_PDB_model_num>'+str(atom['model_no'])+'</PDBx:pdbx_PDB_model_num>\n'
            s+='\t\t\t<PDBx:type_symbol>'+atom['atom_element']+'</PDBx:type_symbol>\n'
            s+='\t\t</PDBx:atom_site>\n'
        s+='\t</PDBx:atom_siteCategory>\n'
        s+='</PDBx:datablock>'
        return s
    
    def write(self, rna_molecule, path_to_file):
        '''
        writes the RNA molecule object to a PDBML/XML file
        '''
        if (not isinstance(rna_molecule, RNA_Molecule)):
            raise TypeError(f"Expected an RNA_Molecule object or a numpy array, got {type(rna_molecule)}")

        processor=Processor()
        atoms = processor.flattenMolecule_to_dict(rna_molecule)  #Get a flat list of atoms (each atom is a dict)

        if isinstance(rna_molecule, RNA_Molecule):
            xml_str=self._format_atom_info(atoms, rna_molecule.entry_id)
            self._wrap_str_to_xml(xml_str, path_to_file)

        print(f"RNA molecule written to {path_to_file}") 





