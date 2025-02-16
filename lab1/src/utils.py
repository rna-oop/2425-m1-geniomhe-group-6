import re
import json
import requests
import os
from Bio import PDB

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