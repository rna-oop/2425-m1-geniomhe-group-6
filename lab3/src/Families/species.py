'''
species module: contains class Species
'''

import sys,os
sys.path.append(os.path.abspath('lab3/src'))



class Species:
    '''
    type Species:

    > Species refer to the organisms (bacteria, animals, plants, etc.) that contain RNA sequences belonging to a particular RNA family
    
    In this class, a species is defined solely by its name. Optionally, it can be defined by its species, genus, family, order, class, phylum, kingdom, and domain.
    All species instances are stored in the declared_species list class attribute to make sure no species is declared twice (equality is based on the name attribute) !!!

    Most important attributes:

    - declared_species [CLASS ATTRIBUTE]: list, contains all the species instances declared so far to avoid duplicates (this allows saving information about a species set of families without isntanciating a family everytime)

    - name: str, name of the species (key attribute, has to b unique for each species, can be named by accession of a sp if needed)
    - rna_molecules: dict, contains all the RNA_Molecule instances that belong to this species

    Everytime we add a the species of an rna-molecule, we also add the rna molecule instance to the species instance (saving all molecules of a species), this is done in the _add_molecule method implicitly to be used from RNA_Molecule module (user should not worry about this; this is why it's a private method)

    helper methods:
    - _get_species: static method, takes a name and returns the species instance with that name if it exists, otherwise returns None (to allow singleton instances with the same name)
    - _add_molecule: method to add an RNA_Molecule instance to the species instance (implicitly called from RNA_Molecule module)

    *validation is handeled in setattr otherwise warning is printed*
    '''
    declared_species = [] #addition will be in setattr after making sure the name is unique

    def __init__(self, name):
        '''
        when initializing a species, we check if the name is unique, if not we return the existing instance with the same name
        does not take any other attributes since we want to keep it simple and only use the name as the key attribute
        '''

        names=[species.name for species in Species.declared_species]
        if name in names:
            print('> note: Species with this name already exists, will return the same instance')
            existing_species = Species._get_species(name)
            self.__dict__ = existing_species.__dict__
                    
        else: #initializing from scratch (no previous instance with the same name)     
            print(f'>> initializing new species: {name} <<')
            self.__name = name
            self.__rna_molecules = {}
            # self.__dict__['_Species__rna_molecules'] = {} #handled teh error in setattr

    def __setattr__(self, name, value): #only handles names bcs no setting of rna_molecules
        if name == '_Species__name':
            value=str(value)
            names=[species.name for species in Species.declared_species]
            if value in names:
                print('Species with this name already exists')
                return
            Species.declared_species.append(self)
        super().__setattr__(name, value)
    

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        print('Warning: name is immutable, cannot be changed; taken as key of an instance, considering deleting the instance and creating a new one')
 
    @property
    def rna_molecules(self):
        return self.__rna_molecules
    @rna_molecules.setter
    def rna_molecules(self, value):
        print('Warning: rna_molecules can not be added froma s pcies level, you should have an RNA_Molecule instance and add its species as attribute, addition will be handled automatically here')
        return #print warning message from __setattr__

    def __str__(self):
        s=f"{self.__name} species"

        return s
    
    def __repr__(self):
        return f'''
        Species(
            name={self.__name},
            rna_molecules={self.__rna_molecules}
        )'''
    
    def __eq__(self, other):
        if not isinstance(other, Species):
            print('Warining: Not the same Species type')
            return False
        return self.__name.lower() == other.name.lower()
    
    def _add_molecule(self, molecule):
        '''
        helper function to add an RNA_Molecule to the species object when it is used in the RNA_Molecule module

        we dont want to add species to RNA_Molecule as well since this will create  a recursive loop, 
        the user must always add an RNA_Molecule from a species instance and addition to the RNA_Molecule instance will be done automatically
        '''
        # --no need to validate RNA_Molecule since this method will be called from RNA_Moelcule class method on self (being of type RNA_Molecule is inevitable)
        if molecule.entry_id not in list(self.__rna_molecules.keys()):
            self.__rna_molecules[molecule.entry_id] = molecule
        else:
            print(f'RNA_Molecule {molecule.entry_id} already exists in the species {self.__name}; not added again')

    @staticmethod
    def _get_species(name):
        for species in Species.declared_species:
            if species.name == name:
                return species
        return None 


if __name__ == '__main__':
    print('test')