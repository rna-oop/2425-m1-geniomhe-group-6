doc='''
utils module conating utilities functions for the RNA library in order to perform data retrieval and file parsing

Functions:
    - parse_newick(newick: str) -> dict: recursively parses a Newick string into a nested dictionary
    - fetch_pdb_file(pdb_entry_id: str, save_directory: str) -> str: fetches a PDB file given a PDB entry ID
    - create_RNA_Molecule(pdb_entry_id: str) -> RNA_Molecule: creates an RNA_Molecule object from a PDB file
    - get_rfam(q: str) -> dict: retrieves information about an RNA family from the RFAM database
    - get_family_attributes(q: str) -> tuple: retrieves attributes of an RNA family from the RFAM database
    - get_pdb_ids_from_fam(fam_id: str) -> list: retrieves the PDB IDs associated with an RNA family
    - get_tree_newick_from_fam(fam_id: str) -> str: retrieves the Newick tree from the RFAM database given the RNA family ID
    
'''

import re
import json
import requests
import os
from Bio import PDB

from Structure.RNA_Molecule import RNA_Molecule
from Structure.Model import Model
from Structure.Chain import Chain
from Structure.Residue import Residue
from Structure.Atom import Atom

CACHE_DIR='.rnalib_cache/'

# -- newick parsing

def parse_newick(newick):
    '''recursively parses a Newick string into a nested dictionar'''
    newick = newick.strip().rstrip(';')  
    return parse_subtree(newick)[0]

def parse_subtree(subtree):
    '''parses a subtree and returns (parsed tree, remaining string)'''
    if not subtree:
        return None, ""

    node = {"branch_length": 0} 
    children = []
    remaining = subtree

    if subtree.startswith("("): 
        subtree = subtree[1:]  
        while subtree:
            child, subtree = parse_subtree(subtree)
            children.append(child)
            if subtree.startswith(","):
                subtree = subtree[1:] 
            elif subtree.startswith(")"):
                subtree = subtree[1:]  
                break

    match = re.match(r"([^\(\),:]+)?(:[\d\.]+)?", subtree)  
    if match:
        name = match.group(1) if match.group(1) else None
        length = float(match.group(2)[1:]) if match.group(2) else 0  

        if name:
            node["name"] = name
            node["name"] = node["name"].strip()
        node["branch_length"] = length
        remaining = subtree[match.end():]

    if children:
        node["children"] = children

    return node, remaining

# -- pdb api biopython

def fetch_pdb_file(pdb_entry_id, save_directory=CACHE_DIR):
    '''
    A function that takes as input pdb entry id and returns the path of the pdb file
    '''
    pdb_entry_id = pdb_entry_id.lower()

    pdb_list = PDB.PDBList()

    target_directory = os.path.join(save_directory, pdb_entry_id)
    
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    pdb_list.retrieve_pdb_file(pdb_entry_id, pdir=target_directory, file_format='pdb')
    
    os.rename(
        os.path.join(target_directory, f'pdb{pdb_entry_id}.ent'),
        os.path.join(target_directory, f'{pdb_entry_id}.pdb')
    )
    
    return os.path.join(target_directory, f'{pdb_entry_id}.pdb')

def create_RNA_Molecule(pdb_entry_id):
    
    pdb_file_path=fetch_pdb_file(pdb_entry_id)
    
    with open(pdb_file_path, 'r') as pdb_file:
        
        experiment = "NA"
        species = "NA"
        
        for line in pdb_file:
            #Extract the EXPDTA (experiment) information
            if line.startswith("EXPDTA"):
                experiment = line[10:].strip()
            
            #Extract the species information
            if line.startswith("SOURCE"):
                if "ORGANISM_SCIENTIFIC" in line:
                    species_info = line.split(":")[1].strip()
                    species = species_info.split(";")[0].strip()
            
            #Stop reading if line starts with "ATOM"
            if line.startswith("ATOM"):
                break  #Exit the loop

    #Create the RNA_Molecule object with the extracted information
    rna_molecule = RNA_Molecule(pdb_entry_id, experiment, species)

    #Continue processing the file to extract the structural information
    with open(pdb_file_path, 'r') as pdb_file:
        
        has_models = False
        current_model = None
        current_chain = None
        current_residue = None
    
        for line in pdb_file:
            if line.startswith("MODEL"):
                has_models = True  #The file contains multiple models
                model_id = int(line.split()[1])  #Extract model ID
                current_model = Model(model_id)  #Create Model object
                rna_molecule.add_model(current_model)  #Store the model
                
            elif line.startswith("ATOM"):
                #Extract chain ID (Column 22 in PDB format)
                chain_id = line[21]  

                #If there are no models, create a default model with ID 0
                if not has_models and current_model is None:
                    current_model = Model(0)
                    rna_molecule.add_model(current_model)

                #If new chain, create and add to current model
                if current_model is not None and (current_chain is None or current_chain.id != chain_id):
                    current_chain = Chain(chain_id)
                    current_model.add_chain(current_chain)

                #Extract residue information (Columns 18-20 for residue name, 23-26 for residue number)
                residue_name = line[17:20].strip()
                #Stop if the residue is not a RNA nucleotide
                if residue_name not in ['A', 'C', 'G', 'U']:
                        break
                residue_id = int(line[22:26].strip())  

                #If new residue, create and add to current chain
                if current_chain is not None and (current_residue is None or current_residue.position != residue_id):
                    current_residue = Residue(residue_name, residue_id)
                    current_chain.add_residue(current_residue)

                #Extract atom details
                atom_name = line[12:16].strip()
                x, y, z = map(float, [line[30:38], line[38:46], line[46:54]])  #Extract coordinates
                element = line[76:78].strip()

                #Create and add Atom object
                atom = Atom(atom_name, x, y, z, element)
                current_residue.add_atom(atom)

    return rna_molecule #Return the RNA_Molecule object that stores the models which is turn store the rest of the structural information


# -- Rfam api: https://docs.rfam.org/en/latest/api.html

r = requests.get('https://rfam.org/family/SAM?content-type=application/json')
print (r.json()['rfam']['acc'])

def get_rfam(q:str):
    r = requests.get(f'https://rfam.org/family/{q}?content-type=application/json')
    return r.json()['rfam']

def get_family_attributes(q:str):
    dt=get_rfam(q)
    name=dt['id']
    identity=dt['acc']
    cur_type=dt['curation']['type']
    return name, identity, cur_type

def get_pdb_ids_from_fam(fam_id):
    '''
    retrieve the PDB IDs associated with an RNA family
    
    Parameters:
        fam_id (str): The RNA family ID.
    
    Returns:
        list: A list of PDB IDs associated with the RNA family.
    '''
    url = f'https://rfam.org/family/{fam_id}/structures?content-type=application/json'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        
        data = response.json()['mapping']
        pdb_ids=[]
        for entry_dict in data:
            pdb_ids.append(entry_dict['pdb_id'])

        return pdb_ids

    except Exception as e:
        return {"Error": str(e)}
    
def get_tree_newick_from_fam(fam_id):
    '''
    get the Newick tree from the RFAM database given the RNA family ID
    returns it in newick_str to facilitate parsing
    '''
    url = f"https://rfam.org/family/{fam_id}/tree/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        
        return response.text

    except Exception as e:
        return str(e)


if __name__=='__main__':
    newick_str = '''
    (87.4_AE017263.1/29965-30028_Mesoplasma_florum_L1[265311].1:0.05592,
    _URS000080DE91_2151/1-68_Mesoplasma_florum[2151].1:0.08277,
        (90_AE017263.1/668937-668875_Mesoplasma_florum_L1[265311].2:0.11049,
        81.3_AE017263.1/31976-32038_Mesoplasma_florum_L1[265311].3:0.31409)
    0.340:0.03601);
    '''

    tree_json = parse_newick(newick_str)

    json_output = json.dumps(tree_json, indent=2)
    print(json_output)
    # cretas file tree.json in test/
    with open('test/tree.json', 'w') as f:
        f.write(json_output)

    print(get_pdb_ids_from_fam('RF00162'))

    print(get_tree_newick_from_fam('RF00162'))

    rna_molecule = create_RNA_Molecule("7EAF")
    # rna_molecule = RNA_Molecule.from_pdb("7EAF") #nop
    rna_molecule.print_all()