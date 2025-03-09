'''
module processor contains class Processor for handling parse/write operations (helper)
'''

import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from Structure.RNA_Molecule import RNA_Molecule
from Structure.Model import Model
from Structure.Chain import Chain
from Structure.Residue import Residue
from Structure.Atom import Atom
from Families.species import Species

import numpy as np

import xml.etree.ElementTree as ET
from xml.dom import minidom

# -- helpers (maybe add to util since related to formatting files)
def wrap_str_to_xml(s,name='pdbml_output.xml'):
    with open(name, "w") as f:
        f.write(s)

def pretty_print_xml(func): #--used as decorator
    def wrapper(*args, **kwargs):
        xml_string = func(*args, **kwargs)
            
        dom = minidom.parseString(xml_string)
            
        pretty_xml = dom.toprettyxml(indent="  ")
            
        return pretty_xml
    return wrapper

class Processor:
    
    def __init__(self):
        self.entry_id = None
        self.experiment = None
        self.species = None
        self.rna_molecule = None
        self.atoms = []
        
    def molecule_info(self, entry_id, experiment, species):
        self.entry_id = entry_id
        if experiment is not None:
            self.experiment = experiment
        if species is not None:
            self.species = Species(species)
        
    def atom_info(self, *args):
        self.atoms.append(list(args))
        
    def createMolecule(self):
        '''
        Creates an RNA molecule object from the parsed information.
        '''
        
        self.rna_molecule = RNA_Molecule(self.entry_id, self.experiment, self.species)
        
        for atom in self.atoms:
            
            atom_name, x, y, z, element, residue_name, residue_id, chain_id, altloc, occupancy, temp_factor, i_code, charge, model_id = atom
            
            self.rna_molecule.add_model(Model(model_id))
            model = self.rna_molecule.get_models()[model_id]
            model.add_chain(Chain(chain_id))
            chain = model.get_chains()[chain_id]
            chain.add_residue(Residue(residue_name, residue_id, i_code=i_code))
            residue = chain.get_residues()[residue_id]
            residue.add_atom(Atom(atom_name, x, y, z, element, altloc, occupancy, temp_factor, charge))
                
        return self.rna_molecule
    

    def createArray(self):
        '''
        Creates a 3D array representation of the RNA molecule.
        The array has dimensions (number of models, number of residues, 3) and stores the x,y,z coordinates of each atom.
        '''
        max_model_id=self.atoms[-1][-1] #access the model_id of the last atom 
        max_res_id=self.atoms[-1][6] #access the res_id of the last atom
        array=np.zeros((max_model_id+1, max_res_id+1, 3)) #initialize the array with zeros
        for atom in self.atoms: 
            model_id, res_id=atom[-1], atom[6] #access the model_id and res_id of the atom
            x, y, z = atom[1:4] #access the x,y,z coordinates of the atom
            array[model_id,res_id]=np.array([x,y,z]) #store the coordinates in the array
        return array
    
        
    def flattenMolecule(self, rna_molecule):
        """
        Flattens the RNA molecule into a list of atoms.
        Each atom is a tuple containing the model ID, serial number, atom, residue and chain.
        """
        atoms = []
        model_id=0
        for model in rna_molecule.get_models().values():
            model_id = model.id
            serial=1
            for chain in model.get_chains().values():
                for residue in chain.get_residues().values():
                    for atom in residue.get_atoms().values():
                        atoms.append((model_id, serial, atom, residue, chain))
                        serial += 1
        return atoms

    def flattenArray(self, array):
        '''
        takes a 3D array RNA Molecule representation (as prviously defined)
        returns a list of atoms

        parameters:
        
        array: numpy array, (3D) dimensions should be 
            - number of models
            - number of residues
            - 3 (values should be each atom's x,y,z coordinates)

        returns:
        
        atoms: list of tuples, each tuple contains 
            - the model ID (default)
            - serial number (index)
            - atom (unknown, X, maybe can add index like X1, X2, etc) in any case here the nth atom is of form [Xn, [x,y,z]] and not an Atom object
            - residue (unkown, UNK) 
            - chain (default, until gaps are introduced)
        '''

        # --removing the initialized 1st nul atom, comment it if array has no longer a nul atom
        if np.all(array[:,0,:]==[0,0,0]):
            array=array[:,1:,:]

        atoms = []
        model_id=0
        chain='X'
        residue='UNK' #or blanks in pdb
        residue_no=1
        atom_name='X'

        for res in array:
            for idx, atom_coord in enumerate(res):
                serial=idx+1
                atom=[atom_name+str(serial), atom_coord]
                atoms.append((model_id, serial, atom, residue+str(residue_no), chain))
            residue_no+=1
        # for idx, atom_coord in enumerate(array[0]): #this takes into consideration that it's of dimensions (1, n, 3)
        #     serial=idx+1
        #     atom=[atom_name+str(serial), atom_coord]
        #     atoms.append((model_id, serial, atom, residue, chain))

        return atoms

    # -- xml processing

    def extract_xml_atoms_from_rna(self, rna_molecule):
        atoms_list = []
        # model = rna_molecule.get_models()[0]  # testing

        for model_num,_ in enumerate(rna_molecule.get_models()):  
            model=rna_molecule.get_models()[_] # --model object from dict key
        
            for chain in model.get_chains().values():  
                for residue in chain.get_residues().values():  
                    for atom_key, atom in residue.get_atoms().items(): 
                        atom_id, alt_id = atom_key  # unpacking atom key (alt_id is '' if no alt location)
                        
                        atom_data = {
                            "id": str(len(atoms_list) + 1),  # Assign a sequential ID
                            "B_iso_or_equiv": str(atom.temp_factor),
                            "Cartn_x": str(atom.x),
                            "Cartn_y": str(atom.y),
                            "Cartn_z": str(atom.z),
                            "auth_asym_id": chain.id,
                            "auth_atom_id": atom_id,
                            "auth_comp_id": residue.type.name,
                            "auth_seq_id": str(residue.position),
                            "group_PDB": "ATOM", # assuming afor now that all are ATOM records
                            "label_alt_id": None if alt_id == "" else alt_id,
                            "label_asym_id": chain.id,
                            "label_atom_id": atom_id,
                            "label_comp_id": residue.type.name,
                            "label_entity_id": "1",  # should be one entity per xml for now
                            "label_seq_id": str(residue.position),
                            "occupancy": str(atom.occupancy),
                            "pdbx_PDB_model_num": model_num+1,
                            "type_symbol": atom.element.name
                        }

                        #if atom.occupancy == 1:
                        #    atom_data["label_alt_id"] = {"xsi:nil": "true"}
                        # --will try adding it in xml formatting
                        
                        atoms_list.append(atom_data)
        
        return atoms_list




    @pretty_print_xml
    def create_xml_from_molecule(self,rna_molecule):
        root = ET.Element("PDBx:datablock", {
            "datablockName": rna_molecule.entry_id,
            "xmlns:PDBx": "http://pdbml.pdb.org/schema/pdbx-v50.xsd",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd"
        })

        atom_site_category = ET.SubElement(root, "PDBx:atom_siteCategory")

        atoms = self.extract_xml_atoms_from_rna(rna_molecule)

        for atom in atoms:
            atom_site = ET.SubElement(atom_site_category, "PDBx:atom_site", {"id": atom["id"]})

            for key, value in atom.items():
                if key == "id":
                    continue
                element = ET.SubElement(atom_site, f"PDBx:{key}")
                if value is None:
                    element.set("xsi:nil", "true")
                else:
                    element.text = str(value)  # Convert value to string

        # tree = ET.ElementTree(root)
        # with open("pdbml_output.xml", "wb") as f:
        #     tree.write(f, encoding="utf-8", xml_declaration=True)

        xml_string = ET.tostring(root, encoding="unicode", method="xml")
        return xml_string


#--testing (non method function stage)
# s=create_xml_from_molecule(rna_molecule)
# wrap_str_to_xml(s)