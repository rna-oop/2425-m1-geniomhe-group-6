'''
PDB_Parser module contains class PDB_Parser for parsing PDB files
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from IO.parsers.RNA_Parser import RNA_Parser
from processor import Processor
from Bio import PDB


class PDB_Parser(RNA_Parser):
    
    def __init__(self):
        pass
    
    def read(self, path_to_file):
        """
        Reads a PDB file and returns the RNA molecule object.
        """
        processor=Processor() #To handle the molecule representation in the processor class
        
        #Extract RNA_Molecule Attributes(Entry_ID, Experiment, Species) and store them in the processor object
        id, experiment, species = self._extract_molecule_info(path_to_file)
        processor.molecule_info(id, experiment, species) 
        
        #Extract the atoms and store them in the processor object
        with open(path_to_file, 'r') as pdb_file:
            
            model_id = 0 
        
            for line in pdb_file:
                if line.startswith("MODEL"):
                    model_id = int(line.split()[1])  #Extract model ID
                    
                elif line.startswith("ATOM"):
                    atom_info = self._extract_atom_info(line)
                    if atom_info is not None:
                        processor.atom_info(*atom_info, model_id)
                    
        return processor.createMolecule() 


    def _extract_atom_info(self, line):
        '''
        Extracts the atom information from an atom line in a PDB file.
        Returns a tuple containing atom information, or None if the residue is not valid.
        '''

        residue_name = line[17:20].strip()
        if residue_name not in ['A', 'C', 'G', 'U']:
            return None #Not a nucleotide
        residue_id = int(line[22:26].strip()) 
        
        atom_name = line[12:16].strip()
        altloc = line[16:17].strip()
        i_code = line[26:27].strip()
        x, y, z = map(float, [line[30:38], line[38:46], line[46:54]])
        occupancy = float(line[54:60].strip())
        temp_factor = float(line[60:66].strip()) if line[60:66].strip() else None
        element = line[76:78].strip()
        charge = line[78:80].strip()
        
        chain_id = line[21]
        
        return atom_name, x, y, z, element, residue_name, residue_id, chain_id, altloc, occupancy, temp_factor, i_code, charge


    def _extract_molecule_info(self, path_to_file):
        """
        Extracts the PDB ID, experiment, and species information from a PDB file.
        """
        with open(path_to_file, 'r') as file:
            
            id = ""
            experiment = None
            species = None
            
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

