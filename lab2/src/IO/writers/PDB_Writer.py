'''
PDB_Write module contains the class PDB_Writer which is responsible for writing the RNA molecule to a PDB file
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from IO.writers.RNA_Writer import RNA_Writer
from processor import Processor

class PDB_Writer(RNA_Writer):
    
    def write(self, rna_molecule, path_to_file):
        """
        Writes the RNA molecule object to a PDB-like file.
        Format:
        <Record name> <Serial> <Atom name> <AltLoc> <Residue name> <ChainID> <Residue sequence number> <ICode> <X> <Y> <Z> <Occupancy> <TempFactor> <Element> <Charge>
        """
        processor=Processor()
        atoms = processor.flattenMolecule(rna_molecule)  #Get a flat list of atoms

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
                pdb_line = self._format_atom_info(*atom_info)
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
        entry_id = rna_molecule.entry_id  
        experiment = rna_molecule.experiment 
        species = rna_molecule.species.name if rna_molecule.species else None
        
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

