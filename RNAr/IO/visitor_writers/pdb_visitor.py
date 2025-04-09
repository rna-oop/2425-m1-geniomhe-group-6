'''
--- PDB Visitor ---
- The PDB visitor is responsible for exporting the RNA_Molecule object to a PDB file
- It implements the Visitor interface
- The export method writes the RNA_Molecule object to a PDB file
- The other methods are helper methods that format the different components of the RNA_Molecule object

- Writes the PDB file in the following format:  
    - HEADER line
    - SOURCE line (if species is provided)
    - EXPDTA line (if experiment is provided)
    - MODEL line
    - ATOM line: <ATOM> <serial> <atom_name> <residue_name> <chain_id> <residue_number> <x> <y> <z> <occupancy> <temp_factor> <element> <charge>
    - ENDMDL line (to close each model)
    - END line (to close the PDB file)
'''



import os,sys
# sys.path.append(os.path.abspath('lab3/src'))

from RNAr.IO.visitor_writers.visitor import Visitor

from RNAr.Structure.RNA_Molecule import RNA_Molecule
from RNAr.Structure.Model import Model
from RNAr.Structure.Chain import Chain
from RNAr.Structure.Residue import Residue
from RNAr.Structure.Atom import Atom

class PDBExportVisitor(Visitor):
    '''
    PDBExportVisitor class implements Visitor interface
    >exports the RNA_Molecule object to a PDB file
    
    methods:
    - write(rna_molecule:RNA_Molecule, path:str) -> None
    - visit_atom(atom: Atom) -> str
    - visit_residue(residue: Residue) -> str
    - visit_chain(chain: Chain) -> str
    - visit_model(model: Model) -> str
    - visit_RNA_Molecule(rna:RNA_Molecule) -> str
    '''
    
    def export(self, rna_molecule:RNA_Molecule, path):
        
        filename=path
        with open(filename, "w") as f:
            
            #Write molecule information
            molecule_info = self.visit_RNA_Molecule(rna_molecule)
            f.write(molecule_info)
            
            #Write pdb line for each atom
            
            current_model = None
            
            for model in rna_molecule.get_models().values():
                model_id=model.id
                model_info = self.visit_Model(model)
                if model_id !=0 and model_id != current_model:
                    if current_model is not None:
                        f.write("ENDMDL\n")  #Close previous model
                    f.write(model_info)
                    current_model = model_id
                serial=1
                #Write the formatted atom line
                for chain in model.get_chains().values():
                    chain_info = self.visit_Chain(chain)
                    for residue in chain.get_residues().values():
                        residue_info = self.visit_Residue(residue)
                        for atom in residue.get_atoms().values():
                            atom_info = self.visit_Atom(atom)
                            pdb_line= f"ATOM  {serial:>5} {atom_info[0]}{residue_info[0]}{chain_info}{residue_info[1]}{atom_info[1]}\n"
                            f.write(pdb_line)
                            serial += 1

            if current_model!=0:
                f.write("ENDMDL\n")  #Close the last model
                
            f.write("END\n")  #End of PDB file
                
        print(f"RNA molecule written to {filename}")
        return None


    def visit_RNA_Molecule(self, rna_molecule):
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
    

    def visit_Atom(self, atom: Atom):
        """
        Formats atom-specific attributes.
        """
        formatted=[]
        
        altloc = atom.altloc or ' '  
        occupancy = atom.occupancy or None  
        temp_factor = atom.temp_factor or None  
        charge = atom.charge or ' '  

        #Format floats or replace with spaces
        occupancy_formatted = f"{occupancy:6.2f}" if isinstance(occupancy, float) else ' ' * 6
        temp_factor_formatted = f"{temp_factor:6.2f}" if isinstance(temp_factor, float) else ' ' * 6  

    
        formatted.append(f"{atom.name:<4}{altloc:1}")
        formatted.append(f"{atom.x:8.3f}{atom.y:8.3f}{atom.z:8.3f}{occupancy_formatted}{temp_factor_formatted}{'':10}{atom.element.value:>2}{charge:2}")
        
        return formatted
        

    def visit_Residue(self, residue: Residue):
        """
        Formats residue-specific attributes.
        """
        formatted=[]
        
        i_code = residue.i_code or ' '
        
        
        formatted.append(f"{residue.type.value:>3} ")
        formatted.append(f"{residue.position:>4}{i_code:1}{'':3}")
        
        return formatted
        
        

    def visit_Chain(self, chain: Chain):
        """
        Formats chain-specific attributes.
        """
        return f"{chain.id:1}"
    

    def visit_Model(self, model: Model): 
        """
        Formats model-specific attributes.
        """
        return f"MODEL     {model.id}\n"


