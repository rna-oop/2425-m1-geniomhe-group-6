doc='''
utils module containing utilities functions for the RNA library in order to perform data retrieval and file parsing

Functions:
    - parse_pdb_files(entries: list) -> np.ndarray: parses a list of PDB entries and returns a numpy array of stacked molecules
    - flattenMolecule(rna_molecule: RNA_Molecule) -> list: flattens the RNA molecule into a list of atoms
    - flattenMolecule_to_dict(rna_molecule: RNA_Molecule) -> list: flattens the RNA molecule into a list of atoms and returns it as a dictionary
    - fetch_pdb_file(pdb_entry_id: str, save_directory: str) -> str: fetches a PDB file given a PDB entry ID
    - parse_newick(newick: str) -> dict: recursively parses a Newick string into a nested dictionary
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
import numpy as np

import os,sys
sys.path.append(os.path.abspath('lab4/src')) 

from Structure.RNA_Molecule import RNA_Molecule
from IO.parsers.PDB_Parser import PDB_Parser


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


def flattenMolecule(rna_molecule:RNA_Molecule):
    """
    Flattens the RNA molecule into a list of atoms.
    Each atom is a tuple containing the model ID, serial number, atom, residue and chain.
    
    helper function in classes that implement the Visitor interface
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

def flattenMolecule_to_dict(rna_molecule:RNA_Molecule):
    atoms_list = []

    for model_num,_ in enumerate(rna_molecule.get_models()):  #--looping through all models 
        model=rna_molecule.get_models()[_] # --model object from dict key
        
        for chain in model.get_chains().values(): #--looping through all chains
            for residue in chain.get_residues().values(): #--looping through all residues  
                for atom_key, atom in residue.get_atoms().items(): #--looping through all atoms
                    atom_id, alt_id = atom_key  # unpacking atom key (alt_id is '' if no alt location)
                    # --keys defined identically to pdbml format, values extracted directly from atom object
                    atom_data = {
                        "atom_id": str(len(atoms_list) + 1),  # Assign a sequential ID
                        "B": str(atom.temp_factor),
                        "x": str(atom.x),
                        "y": str(atom.y),
                        "z": str(atom.z),
                        "chain_id": chain.id,
                        "atom_id": atom_id,
                        "residue_type": residue.type.name,
                        "residue_pos": str(residue.position),
                        "alt_id": None if alt_id == "" else alt_id,
                        "occupancy": str(atom.occupancy),
                        "model_no": model_num+1,
                        "atom_element": atom.element.name
                    }
                    atoms_list.append(atom_data)
    return atoms_list




def parse_pdb_files(entries: list):
    """
    Parses a list of PDB entries and returns a numpy array of stacked molecules.
    Dimension: (number of files including different models, number of residues, number of atoms, 3)
    """
    
    parser = PDB_Parser()
    all_molecules = []
    all_sequences = []
    
    for entry in entries:
        pdb_path_test = fetch_pdb_file(entry)
        mol = parser.read(pdb_path_test, "PDB")
        all_molecules.append(mol[1])
        all_sequences.append(mol[0])

    max_residues = max(mol.shape[1] for mol in all_molecules)
    max_atoms = max(mol.shape[2] for mol in all_molecules)

    padded_molecules = []
    
    for mol in all_molecules:
        padded = np.full((mol.shape[0], max_residues, max_atoms, 3), np.nan)
        padded[:, :mol.shape[1], :mol.shape[2], :] = mol
        padded_molecules.append(padded)

    stacked_molecules = np.vstack(padded_molecules)
    
    padded_sequences = []
    
    for seq in all_sequences:
        padded = np.full((seq.shape[0], max_residues), "", dtype=object)
        padded[:, :seq.shape[1]] = seq
        padded_sequences.append(padded)
        
    stacked_sequences = np.vstack(padded_sequences)
    
    return stacked_sequences, stacked_molecules

pathify_pdb=fetch_pdb_file

if __name__=='__main__':
    
    """
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

    """

    array, seq=parse_pdb_files(['7eaf', '1r7w'])
    print(array.shape)
    print(seq.shape)
    print(seq)