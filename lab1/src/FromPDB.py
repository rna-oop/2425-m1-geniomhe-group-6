from Bio import PDB
import os

from RNA_Molecule import RNA_Molecule
from Model import Model
from Chain import Chain
from Residue import Residue
from Atom import Atom


def fetch_pdb_file(pdb_entry_id, save_directory='lab1/data'):
    '''
    A function that takes as input pdb entry id and returns the path of the pdb file
    '''
    #Ensure the pdb_entry_id is in lowercase as the PDB ID is case-sensitive
    pdb_entry_id = pdb_entry_id.lower()

    #Initialize PDBList to handle the retrieval of the PDB file
    pdb_list = PDB.PDBList()

    #Specify the directory where the file should be saved
    target_directory = os.path.join(save_directory, pdb_entry_id)
    
    #Create the directory if it does not exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    #Retrieve the PDB file in PDB format and save it to the directory
    pdb_list.retrieve_pdb_file(pdb_entry_id, pdir=target_directory, file_format='pdb')
    
    #Rename the downloaded file to match the PDB ID
    os.rename(
        os.path.join(target_directory, f'pdb{pdb_entry_id}.ent'),
        os.path.join(target_directory, f'{pdb_entry_id}.pdb')
    )
    
    #Return the path to the saved PDB file
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



#Example usage:
rna_molecule = create_RNA_Molecule("7EAF")
rna_molecule.print_all()


