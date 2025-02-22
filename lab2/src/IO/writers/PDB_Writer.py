'''
PDB_Write module contains the class PDB_Writer which is responsible for writing the RNA molecule to a PDB file
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from IO.writers.RNA_Writer import RNA_Writer

class PDB_Writer(RNA_Writer):
    
    def write(self, rna_molecule, path_to_file):
        """
        Writes the RNA molecule object to a PDB file.
        """
        with open(path_to_file, "w") as f:
            for model in rna_molecule.get_models().values():
                serial = 1 
                for chain in model.get_chains().values():
                    for residue in chain.get_residues().values():
                        for atom in residue.get_atoms().values():
                            altloc = atom.altloc if atom.altloc is not None else ' '  #Use space for empty column
                            occupancy = atom.occupancy if atom.occupancy is not None else ' '  #Use space for empty column
                            temp_factor = atom.temp_factor if atom.temp_factor is not None else ' '  #Use space for empty column
                            i_code = atom.i_code if atom.i_code is not None else ' '  #Use space for empty column
                            charge = atom.charge if atom.charge is not None else ' '  #Use space for empty column

                            #Format the float if present, else it will be space
                            occupancy_formatted = f"{occupancy:6.2f}" if isinstance(occupancy, float) else ' '*6
                            temp_factor_formatted = f"{temp_factor:6.2f}" if isinstance(temp_factor, float) else ' '*6 

                            f.write(
                                f"ATOM  {serial:>5} {atom.name.value:<4}{altloc:1}{residue.type.value:>3} "
                                f"{chain.id:1}{residue.position:>4}{i_code:1}   "
                                f"{atom.x:8.3f}{atom.y:8.3f}{atom.z:8.3f}"
                                f"{occupancy_formatted}{temp_factor_formatted}          "
                                f"{atom.element.value:>2}{charge:2}\n"
                            )
                            serial += 1  #Increment serial for each atom
        print(f"RNA molecule written to {path_to_file}")
