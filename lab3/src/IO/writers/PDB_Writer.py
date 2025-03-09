'''
PDB_Write module contains the class PDB_Writer which is responsible for writing the RNA molecule to a PDB file
'''

from typing import Union
import os,sys
sys.path.append(os.path.abspath('lab3/src'))

from IO.writers.RNA_Writer import RNA_Writer
from Structure.RNA_Molecule import RNA_Molecule
from processor import Processor

import numpy as np


# helper
def is_RNA_mol(rna_molecule):
    if isinstance(rna_molecule, RNA_Molecule):
        return True
    return False



class PDB_Writer(RNA_Writer):
    '''
    class PDB_Writer inherits the abstract class RNA_Writer:
    > enforced to implement the abstract method write()

    it's responsible for writing the RNA molecule to a PDB file
    allow the user to give it either an RNA_Molecule object or a numpy array representing the RNA molecule
    '''
    
    def write(self, rna_molecule: Union[RNA_Molecule, np.ndarray], path_to_file):
        """
        Writes the RNA molecule object to a PDB-like file.
        Format:
        <Record name> <Serial> <Atom name> <AltLoc> <Residue name> <ChainID> <Residue sequence number> <ICode> <X> <Y> <Z> <Occupancy> <TempFactor> <Element> <Charge>
        """
        if (not is_RNA_mol(rna_molecule)) and (type(rna_molecule) is not np.ndarray):
            raise TypeError(f"Expected an RNA_Molecule object or a numpy array, got {type(rna_molecule)}")

        processor=Processor()

        if type(rna_molecule) is np.ndarray:
            print(' -- writing from array -- ')
            flattening=processor.flattenArray  #Get a flat list of atoms where 
            formatting=self._format_atom_info_for_array
                # --each item is of the form: model_id, serial, atom, residue, chain 
                # --(atom of form [Xn, [x, y, z]])

        else:
            print(' -- writing from object -- ')
            flattening=processor.flattenMolecule  #this function Get a flat list of atoms (with actual objects)
            formatting=self._format_atom_info #this function formats an atom entry into PDB format line

        # -- common steps for both implementations --
        atoms = flattening(rna_molecule)  #Get a flat list of atoms

        with open(path_to_file, "w") as f:
                    
            #Write molecule information
            molecule_info = self._format_molecule_info(rna_molecule)
            f.write(molecule_info)
                    
            #Write atom information
                    
            current_model = None

            for model_id, *atom_info in atoms:
                #Write MODEL record when a new model starts
                #If the model ID is 0, it means that there is only one model and no MODEL record is needed
                if model_id !=0 and model_id != current_model:
                    if current_model is not None:
                        f.write("ENDMDL\n")  #Close previous model
                    f.write(f"MODEL     {model_id}\n")
                    current_model = model_id
                        
                #Write the formatted atom line
                pdb_line = formatting(*atom_info)
                f.write(pdb_line)

            if model_id!=0:
                f.write("ENDMDL\n")  #Close the last model
            f.write("END\n")  #End of PDB file

        print(f"RNA molecule written to {path_to_file}")


    def _format_atom_info(self, serial, atom, residue, chain):
        """
        Formats an atom entry into PDB format.
        """
        altloc = atom.altloc or ' '  
        occupancy = atom.occupancy or None  
        temp_factor = atom.temp_factor or None  
        i_code = residue.i_code or ' '  
        charge = atom.charge or ' '  

        #Format floats or replace with spaces
        occupancy_formatted = f"{occupancy:6.2f}" if isinstance(occupancy, float) else ' ' * 6
        temp_factor_formatted = f"{temp_factor:6.2f}" if isinstance(temp_factor, float) else ' ' * 6  

        return (
            f"ATOM  {serial:>5} {atom.name.value:<4}{altloc:1}{residue.type.value:>3} "
            f"{chain.id:1}{residue.position:>4}{i_code:1}{'':3}"
            f"{atom.x:8.3f}{atom.y:8.3f}{atom.z:8.3f}"
            f"{occupancy_formatted}{temp_factor_formatted}{'':10}"
            f"{atom.element.value:>2}{charge:2}\n"
        )


    def _format_molecule_info(self, rna_molecule):
        """
        Formats molecule information (entry_id, experiment, species) in PDB format.
        """
        lines = []
        
        #Extract information from the RNA molecule
        if is_RNA_mol(rna_molecule):
            entry_id = rna_molecule.entry_id  
            experiment = rna_molecule.experiment 
            species = rna_molecule.species.name if rna_molecule.species else None

        else:
            entry_id = "????"  #check how to assign this
            experiment = None  
            species = None
        
        #Format HEADER line
        header_line = f"HEADER    RNA{'':49}{entry_id:4}"
        lines.append(header_line)

        #Format SOURCE line if species is provided
        if species:
            source_line = f"SOURCE    ORGANISM_SCIENTIFIC: {species:<65}"
            lines.append(source_line)
            
        #Format EXPDTA line if experiment is provided
        if experiment:
            expdta_line = f"EXPDTA    {experiment:<69}"
            lines.append(expdta_line)

        return "\n".join(lines) + "\n"


    def _format_atom_info_for_array(self, serial, atom, residue, chain):
        '''
        all inputs are of primitive types, no objects involved as in _format_atom_info,
        the sole purpose of this function is to present a parallel implementation to _format_atom_info as a formatting function for the array representation
        *this helper will be used in the write method when the input is a numpy array, by setting the formatting variable to this function when type is ndarray*
        '''
        atom_name=atom[0]
        x,y,z=coord=atom[1]
        residue_position=-1

        altloc = ' '  
        occupancy = None  
        temp_factor = None  
        i_code = ' '  
        charge =' '  

        #Format floats or replace with spaces
        occupancy_formatted = f"{occupancy:6.2f}" if isinstance(occupancy, float) else ' ' * 6
        temp_factor_formatted = f"{temp_factor:6.2f}" if isinstance(temp_factor, float) else ' ' * 6  

        return (
            f"ATOM  {serial:>5} {atom_name:<4}{altloc:1}{residue:>3} "
            f"{chain:1}{residue_position:>4}{i_code:1}{'':3}"
            f"{x:8.3f}{y:8.3f}{z:8.3f}"
            f"{occupancy_formatted}{temp_factor_formatted}{'':10}"
            f"{atom_name:>2}{charge:2}\n"
        )