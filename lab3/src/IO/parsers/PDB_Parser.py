'''
PDB_Parser module contains class PDB_Parser for parsing PDB files
'''

import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from IO.parsers.RNA_Parser import RNA_Parser
from processor import Processor


class PDB_Parser(RNA_Parser):
    
    def __init__(self):
        pass
    
    def read(self, path_to_file, coarse_grained=False, atom_name="C1'", array=True):
        """
        Reads a PDB file and returns the RNA molecule object.
        """
        processor=Processor() #To handle the molecule representation in the processor class
        
        #Extract RNA_Molecule Attributes and store them in the processor object
        molecule_info = self._extract_molecule_info(path_to_file)
        processor.molecule_info(*molecule_info)
        
        #Extract the atoms and store them in the processor object
        with open(path_to_file, 'r') as pdb_file:
            
            model_id = 0 
        
            for line in pdb_file:
                if line.startswith("MODEL"):
                    model_id = int(line.split()[1])  #Extract model ID
                    
                elif line.startswith("ATOM"):
                    if coarse_grained:
                        if line[12:16].strip() == atom_name:
                            atom_info = self._extract_atom_info(line)
                            if atom_info is not None:
                                processor.atom_info(*atom_info, model_id)
                    else:
                        atom_info = self._extract_atom_info(line)
                        if atom_info is not None: #It is None if the residue is not a nucleotide
                            processor.atom_info(*atom_info, model_id)
                            
        if array:
            return processor.createArray()
        else:         
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
        i_code = line[26:27].strip()
        
        atom_name = line[12:16].strip()
        altloc = line[16:17].strip()
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
            check_next_line = False
            
            for line in file:
                
                #Extract the PDB ID
                if line.startswith("HEADER"):
                    id = line[62:66].strip()
                    
                #Extract the EXPDTA (experiment) information
                if line.startswith("EXPDTA"):
                    experiment = line[10:].strip()
                
                #Extract the species information
                if line.startswith("SOURCE"):
                    if check_next_line:
                        #Extract everything after the first two words (SOURCE and index)
                        sp_second_part = " ".join(line.split()[2:]).rstrip(";")
                        species += " " + sp_second_part
                        check_next_line = False
                    else:
                        if "ORGANISM_SCIENTIFIC" in line:
                            species_info = line.split(":")[1].strip()
                            if ";" in species_info:
                                species = species_info.split(";")[0].strip()
                            else:
                                species = species_info.strip()  #Store the incomplete name
                                check_next_line = True  # Flag to check the next line
                            
                        
                if line.startswith("REMARK") | line.startswith("ATOM"):
                    break
                
        return id, experiment, species