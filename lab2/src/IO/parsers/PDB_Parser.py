from IO.parsers.RNA_Parser import RNA_Parser
from processor import Processor
from Bio import PDB
import os

class PDB_Parser(RNA_Parser):
    
    def __init__(self):
        pass
    
    def read(self, path_to_file, extract_residues=True, extract_chains=True):
        """
        Reads a PDB file and returns the RNA molecule object.
        """
        processor=Processor() #To handle the molecule representation in the processor class
        
        #Extract RNA_Molecule Attributes(Entry_ID, Experiment, Species) and store them in the processor object
        processor.rna_info(self.extract_molecule_info(path_to_file)) 
        
        #Extract the atoms and store them in the processor object
        with open(path_to_file, 'r') as pdb_file:
            
            model_id = 0 
        
            for line in pdb_file:
                if line.startswith("MODEL"):
                    model_id = int(line.split()[1])  #Extract model ID
                    
                elif line.startswith("ATOM"):
                    atom_info = self.extract_atom_info(line, extract_residues, extract_chains)
                    if atom_info is not None:
                        processor.atom_info(*atom_info, model_id)
                    
        return processor.createMolecule() 
    
    
    
    

    def _extract_atom_info(line, extract_residue, extract_chain):
        '''
        Extracts the atom information from an atom line in a PDB file.
        Parameters:
        - line: A string representing a line from a PDB file.
        - extract_residues: Boolean to specify if residue information should be extracted.
        - extract_chains: Boolean to specify if chain information should be extracted.
        Returns:
        - A tuple containing atom information, or None if the residue is not valid.
        '''
        if extract_chain:
            chain_id = line[21]
    
        if extract_residue:
            residue_name = line[17:20].strip()
            if residue_name not in ['A', 'C', 'G', 'U']:
                return None #Not a nucleotide
            residue_id = int(line[22:26].strip()) 

        atom_name = line[12:16].strip()
        x, y, z = map(float, [line[30:38], line[38:46], line[46:54]])
        element = line[76:78].strip()

        #Construct the return tuple based on what is extracted
        if extract_residue and extract_chain:
            return atom_name, x, y, z, element, residue_name, residue_id, chain_id
        elif extract_residue:
            return atom_name, x, y, z, element, residue_name, residue_id
        elif extract_chain:
            return atom_name, x, y, z, element, chain_id
        else:
            return atom_name, x, y, z, element  #Only return atom information




    
    def _extract_molecule_info(path_to_file):
        """
        Extracts the PDB ID, experiment, and species information from a PDB file.
        """
        with open(path_to_file, 'r') as file:
            
            id = "NA"
            experiment = "NA"
            species = "NA"
            
            for line in file:
                
                #Extract the PDB ID
                if line.startswith("HEADER"):
                    id = line[62:66].strip()
                    
                #Extract the EXPDTA (experiment) information
                if line.startswith("EXPDTA"):
                    experiment = line[10:].strip()
                
                #Extract the species information
                if line.startswith("SOURCE"):
                    if "ORGANISM_SCIENTIFIC" in line:
                        species_info = line.split(":")[1].strip()
                        species = species_info.split(";")[0].strip()
                        
                if line.startswith("REMARK") | line.startswith("ATOM"):
                    break
                
        return id, experiment, species
                        
        
    
    
    
    
    
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