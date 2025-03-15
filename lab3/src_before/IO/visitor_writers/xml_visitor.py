'''
--- XMLVisitor ---
module containing the XMLExportVisitor class
>implements the Visitor interface
>responsible for exporting the RNA_Molecule object to an PDML/XML file
'''

import os,sys
sys.path.append(os.path.abspath('lab3/src'))
from Structure.RNA_Molecule import RNA_Molecule
from utils import flattenMolecule_to_dict

from IO.visitor_writers.visitor import Visitor

class XMLExportVisitor(Visitor):
    '''
    Visitor class that implements the Visitor interface
    >responsible for exporting the RNA_Molecule object to an PDML/XML file

    methods:
        visit_RNA_Molecule(rna:RNA_Molecule) -> None
    '''

    def __init__(self):
        pass

    def visit_RNA_Molecule(self, rna_molecule:RNA_Molecule):
        '''
        method that allows the visitor to visit the RNA_Molecule object and export it to an XML file
        '''
        atoms=flattenMolecule_to_dict(rna_molecule)
        with open(rna_molecule.entry_id+"_PDBMLified.xml", "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            f.write(f'''<PDBx:datablock datablockName="{rna_molecule.entry_id}"
   xmlns:PDBx="http://pdbml.pdb.org/schema/pdbx-v50.xsd"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd">
''')
            f.write('\t<PDBx:atom_siteCategory>\n')
            for atom in atoms:
                
                f.write(f'''\t\t<PDBx:atom_site id="{atom["atom_id"]}">
         <PDBx:B_iso_or_equiv>{atom['B']}</PDBx:B_iso_or_equiv>
         <PDBx:Cartn_x>{atom['x']}</PDBx:Cartn_x>
         <PDBx:Cartn_y>{atom['y']}</PDBx:Cartn_y>
         <PDBx:Cartn_z>{atom['z']}</PDBx:Cartn_z>
         <PDBx:auth_asym_id>{atom['chain_id']}</PDBx:auth_asym_id>
         <PDBx:auth_atom_id>{atom['atom_id']}</PDBx:auth_atom_id>
         <PDBx:auth_comp_id>{atom['residue_type']}</PDBx:auth_comp_id>
         <PDBx:auth_seq_id>{atom['residue_pos']}</PDBx:auth_seq_id>
         <PDBx:group_PDB>ATOM</PDBx:group_PDB>''')
                
                if atom['alt_id'] is not None:
                    f.write('<PDBx:label_alt_id xsi:nil="true" />\n')
                else:
                    atom['alt_id']='A' #saving it to place it later
                
                f.write(f'''<PDBx:label_asym_id>{atom['alt_id']}</PDBx:label_asym_id>
         <PDBx:label_atom_id>{atom['atom_id']}</PDBx:label_atom_id>
         <PDBx:label_comp_id>{atom['residue_type']}</PDBx:label_comp_id>
         <PDBx:label_entity_id>1</PDBx:label_entity_id>
         <PDBx:label_seq_id>{atom['residue_pos']}</PDBx:label_seq_id>
         <PDBx:occupancy>{atom['occupancy']}</PDBx:occupancy>
         <PDBx:pdbx_PDB_model_num>{atom['model_no']}</PDBx:pdbx_PDB_model_num>
         <PDBx:type_symbol>{atom['atom_element']}</PDBx:type_symbol>
      </PDBx:atom_site>''')                        
                f.write('''  </PDBx:atom_siteCategory>
</PDBx:datablock>''')
