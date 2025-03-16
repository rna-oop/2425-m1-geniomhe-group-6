'''
--- XMLVisitor ---
module containing the XMLExportVisitor class
>implements the Visitor interface
>responsible for exporting the RNA_Molecule object to an PDML/XML file
'''

import os,sys
sys.path.append(os.path.abspath('lab3/src'))
from Structure.RNA_Molecule import RNA_Molecule
from Structure.Model import Model
from Structure.Chain import Chain
from Structure.Residue import Residue
from Structure.Atom import Atom

from IO.visitor_writers.visitor import Visitor


def _indent(s:str,n:int=0)->str:
    '''vanilla is just to add a \n to the end of the string'''
    s='\t'*n+s+'\n'
    return s

class XMLExportVisitor(Visitor):
    '''
    Visitor class that implements the Visitor interface
    >responsible for exporting the RNA_Molecule object to an PDML/XML file

    methods:
    - visit_RNA_Molecule(rna:RNA_Molecule) -> 
    '''
    def export(self, rna_molecule:RNA_Molecule, path:str)->None:
        '''
        method to export the RNA_Molecule object to a file
        
        xml file order of atom_site Category:
        - atom 0: B_iso_or_equiv (temp_factor)
        - atom 1: Cartn_x (x)
        - atom 2: Cartn_y (y)
        - atom 3: Cartn_z (z)
        - chain 0: auth_asym_id (chain_id)
        - atom 4: auth_atom_id (atom_name)
        - residue 0: auth_comp_id (residue_type)
        - residue 1: auth_seq_id (residue_pos)
        - FIXED group_PDB: ATOM 
        - atom 5 
            - true flag if alt does not exists 
            - label_alt_id (alt_id) else
        - chain 1: label_asym_id (chain id)
        - atom 6: label_atom_id (atom_name)
        - residue 2: label_comp_id (residue_type)
        - FIXED label_entity_id: 1 
        - residue 3: label_seq_id (residue_pos)
        - atom 7: occupancy
        - model: pdbx_PDB_model_num (model_id)
        - atom 8: type_symbol (element)
        '''
        filename=path
        if not filename.endswith('.xml'):
            filename+='.xml'

        with open(filename, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            
            header=self.visit_RNA_Molecule(rna_molecule)
            f.write(_indent(header))
            
            f.write(_indent('<PDBx:atom_siteCategory>',1))

            site_id=0

            for model in rna_molecule.get_models().values():
                model_info=self.visit_Model(model)

                for chain in model.get_chains().values():
                    chain_info=self.visit_Chain(chain)

                    for residue in chain.get_residues().values():
                        residue_info=self.visit_Residue(residue)

                        for atom in residue.get_atoms().values():
                            # atom_id, alt_id = atom_key
                            site_id+=1

                            atom_info=self.visit_Atom(atom)

                            f.write(_indent(f'<PDBx:atom_site id="{site_id}">',2))

                            f.write(_indent(atom_info[0],3))
                            f.write(_indent(atom_info[1],3))
                            f.write(_indent(atom_info[2],3))
                            f.write(_indent(atom_info[3],3))
                            f.write(_indent(chain_info[0],3))
                            f.write(_indent(atom_info[4],3))
                            f.write(_indent(residue_info[0],3))
                            f.write(_indent(residue_info[1],3))
                            f.write(_indent('<PDBx:group_PDB>ATOM</PDBx:group_PDB>',3))

                            f.write(_indent(atom_info[5],3)) #-- adding flag which is added at the end

                            f.write(_indent(chain_info[1],3))

                            f.write(_indent(atom_info[6],3))
                            f.write(_indent(residue_info[2],3))
                            f.write(_indent('<PDBx:label_entity_id>1</PDBx:label_entity_id>',3))
                            f.write(_indent(residue_info[3],3))
                            f.write(_indent(atom_info[7],3))
                            f.write(_indent(model_info,3))
                            f.write(_indent(atom_info[8],3))


                            f.write(_indent('</PDBx:atom_site>',2))

            f.write(_indent('</PDBx:atom_siteCategory>',1))
            f.write('</PDBx:datablock>')

    def visit_RNA_Molecule(self, rna_molecule:RNA_Molecule)->str:
        '''
        method that allows the visitor to visit the RNA_Molecule object and returns its XML formatted string
        '''

        entry_id=rna_molecule.entry_id
        return f'<PDBx:datablock xmlns:PDBx="http://pdbml.pdb.org/schema/pdbx-v50.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" datablockName="{entry_id:4}" xsi:schemaLocation="http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd">'

    def visit_Model(self, model:Model)->str:
        '''
        takes a Model object and returns its respective XML formatted string
        '''

        model_num=model.id
        if model_num==0:
            model_num=1

        return f'<PDBx:pdbx_PDB_model_num>{model_num}</PDBx:pdbx_PDB_model_num>'

    
    def visit_Chain(self, chain:Chain):
        chain_id=chain.id #letter not a number
        formatted=[]

        formatted.append(f'<PDBx:auth_asym_id>{chain_id}</PDBx:auth_asym_id>')
        formatted.append(f'<PDBx:label_asym_id>{chain_id}</PDBx:label_asym_id>')

        return formatted


    
    def visit_Residue(self, residue:Residue):
        formatted=[]

        formatted.append(f'<PDBx:auth_comp_id>{residue.type.value}</PDBx:auth_comp_id>')
        formatted.append(f'<PDBx:auth_seq_id>{residue.position}</PDBx:auth_seq_id>')

        formatted.append(f'<PDBx:label_comp_id>{residue.type.value}</PDBx:label_comp_id>')
        formatted.append(f'<PDBx:label_seq_id>{residue.position}</PDBx:label_seq_id>')

        return formatted

    
    def visit_Atom(self, atom:Atom):
        formatted=[]

        altloc = atom.altloc #if there is no altloc, set it to A  (laters)
        flag=''

        formatted.append(f'<PDBx:B_iso_or_equiv>{atom.temp_factor}</PDBx:B_iso_or_equiv>')

        formatted.append(f'<PDBx:Cartn_x>{atom.x}</PDBx:Cartn_x>')
        formatted.append(f'<PDBx:Cartn_y>{atom.y}</PDBx:Cartn_y>')
        formatted.append(f'<PDBx:Cartn_z>{atom.z}</PDBx:Cartn_z>')

        formatted.append(f'<PDBx:auth_atom_id>{atom.name}</PDBx:auth_atom_id>')

        if altloc == '':
            flag='<PDBx:label_alt_id xsi:nil="true"/>'
            formatted.append(flag)
            altloc='A'        
        else:
            formatted.append(f'<PDBx:label_alt_id>{altloc}</PDBx:label_alt_id>')    

        

        formatted.append(f'<PDBx:label_atom_id>{atom.name}</PDBx:label_atom_id>')

        formatted.append(f'<PDBx:occupancy>{atom.occupancy}</PDBx:occupancy>')
        formatted.append(f'<PDBx:type_symbol>{atom.element.name}</PDBx:type_symbol>')

        # if flag!='':
        #     formatted.append(flag)

        return formatted