__doc__='''
family module contains class Family
'''

import os,sys
sys.path.append(os.path.abspath('lab2/src'))

from Structure.RNA_Molecule import RNA_Molecule
from Families.tree import Phylotree
from utils import get_family_attributes, create_RNA_Molecule, get_tree_newick_from_fam

import pandas as pd

class Family:
    '''
    --- Family class ---
    --------------------

    This class represents a family of RNA molecules. 

    > A  RNA  family  (in  the  Rfam  database)  consists  of  evolutionarily  related  RNA  sequences  sharing  commonsequence  similarity,  secondary  structure,  and  often  function.  Some  of  the  families  featured  in  the  Rfamdatabase  include  rRNA  (Ribosomal  RNA);  tRNA  (Transfer  RNA),  which  is essential  for  protein  translation;miRNA (MicroRNA), which are regulatory RNAs that inhibit gene expression; and Other ncRNAs (Non-codingRNAs).  The  RNA  structure  7EAF  described  earlier  belongs  to  the  SAM  riboswitch  Rfam  family.  Moreinformation about this family can be found here:https://rfam.org/family/SAM.

    This class has the following attributes:
    - Class attributes:
        - entries: list of Family objects, representing all the families created to keep track and avoid duplicates
    - Instance attributes:
        - id: str, representing the family id (unique)
        - name: str, representing the family name
        - type: str, representing the family type 
        - members: list of RNA_Molecule objects, representing the family members
        - trees: dict of Phylotree objects, representing the family trees 

    This class has the following methods:

    - helper methods:
        - __validate_member(member): validate if the member is an instance of RNA_Molecule
        - __validate_tree(tree): validate if the tree is an instance of Phylotree 
        - __delete_family(id): delete the family with the given id from the entries list

    - instance methods:
        - `add_RNA(self, RNA)`
        - `remove_RNA(self, RNA)`


    - class methods:
        - `get_instances()`
        - `get_family(id)`

    - dunders:
        - `__init__(id, name, type=None, members=[], from_database=False)`
            > from_database is a flag to indicate if the object is created using the generator function from the database 
        - `__del__(self)`
        - `__eq__(self, other)`
        - `__len__(self)`
        - `__getitem__(self, key)`
        - `__setattr__(self, name, value)`
        - `__str__(self)`
        - `__repr__(self)`
    '''

    # --class attribute to store all families - no duplicates are allowed (checked in __setattr__), unique by id
    entries=[] 

    def __init__(self, id, name, type=None, members=[], trees={}, from_database=False):
        if not from_database:
            print('Warning: Family object created without database connection, creating a new family with provided id and name')

        ids = [entry.id for entry in Family.entries]
        if id in ids:  # do not instantiate if family with this id already exists, return the existing instance (by reference)
            print(f'Family with this id already exists, will link it to the existing family')
            existing_family = Family.get_family(id)
            self=existing_family
            self.__dict__ = existing_family.__dict__
        else:
            self.__id = id
            self.__name = name
            self.__type = type
            self.__members = members  # list of RNA_Molecule objects
            self.__trees = trees
            self.__clan=None
            Family.entries.append(self)  # adding it to list of instances
            print('Family created successfully')

    # helpers:
    def __validate_member(self, member):
        if not isinstance(member, RNA_Molecule):
            raise ValueError('Member must be an instance of RNA_Molecule')
    @staticmethod
    def __delete_family(id): #only removes it from entries, used in __del__
        for entry in Family.entries:
            if entry.id == id:
                Family.entries.remove(entry)
                return
        print('Family not found')
            
    def __validate_tree(self, tree):
        if not isinstance(tree, Phylotree):
            raise ValueError('Tree must be an instance of Phylotree')

    
    # --getters/setters decorators
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        print('Warning: id is immutable, cannot be changed')

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def members(self):
        return self.__members
    @members.setter
    def members(self, value):
        self.__members = value

    @property
    def trees(self):
        return self.__trees
    @trees.setter
    def trees(self, value):
        self.__trees = value

    @property
    def clan(self):
        return self.__clan
    @clan.setter
    def clan(self, value):
        print('Warning: cannot set clan from family level, please use the Clan class to set the clan for this family\n\t e.g., c1.add_family(f1) # will be automatically added to f1')

    # --dunders
    def __eq__(self, other):
        return self.id == other.id

    def __len__(self):
        return len(self.__members)

    def __getitem__(self, key):
        '''make it indexable to access members by index'''
        if key >= len(self.__members):
            raise IndexError('Index out of range')
        return self.__members[key]
        
    
    def __setattr__(self, name, value):
        if name == '_Family__id':
            id_entries=[entry.id for entry in Family.entries]
            if value in id_entries:
                raise ValueError('Family with id '+value+' already exists, please choose another id')
            else:
                value=str(value)
                super().__setattr__(name, value)
        elif name=='_Family__name':
            value=str(value)
            super().__setattr__(name, value)
        elif name=='_Family__type':
            value=str(value)
            super().__setattr__(name, value)
        elif name=='_Family__members':
            if not isinstance(value, list):
                raise ValueError('Members must be a list of RNA_Molecule objects')
            for member in value:
                self.__validate_member(member)
            super().__setattr__(name, value)
        elif name=='_Family__trees':
            # dict of trees
            if not isinstance(value, dict):
                raise ValueError('Trees must be a dictionary of Phylotree objects')
            for key in value:
                self.__validate_tree(value[key])
            super().__setattr__(name, value)
        elif name=='_Family__clan':
            super().__setattr__(name, value)
            #to be able to set it from clan level


    def __str__(self):
        fam='-- Family: '+self.name+' ('+self.id+')\n'
        if self.type:
            fam+='\tType: '+self.type+'\n'
        if self.clan:
            fam+='\tClan: '+self.clan.name
        if self.members != []:
            fam+='\tMembers:\n'
            for member in self.members:
                fam+='\t\t'+str(member)+'\n'
        if self.trees:
            fam+='\tTrees:\n'
            for k,v in self.trees.items():
                fam+='\t\t'+k+':\n'+str(v)+'\n'
        return fam

    def __repr__(self):
        return f'''
        Family(
            id={self.id}, 
            name={self.name}, 
            type={self.type}, 
            members={self.members},
            trees={self.trees}
        )'''
    
    # -- instance methods
    def add_RNA(self, RNA):
        self.__validate_member(RNA)
        if RNA not in self.__members:
            self.__members.append(RNA)
        else:
            print('RNA molecule already in family')

    def remove_RNA(self, RNA):
        if RNA in self.__members:
            self.__members.remove(RNA)
        else:
            print('RNA molecule not in family')

    def add_tree(self, tree, method='NA', format='nwk'):
        '''
        takes a tree from user, it can be of types:
        - Phylotree
        - dict
        - str

        if it's a string it should be either newick or json string/file path

        param:
        - tree: Phylotree, dict or str
        - method: str, representing the method/db used to generate the tree (default='NA')
        - format: str, representing the format of the tree if it's a string (default='nwk' for newick)

        '''
        if isinstance(tree, Phylotree):
            self.__trees[method]=tree
        elif isinstance(tree, dict):
            treefied=Phylotree.from_dict(tree)
            self.__trees[method]=treefied
        elif isinstance(tree, str):
            if format=='nwk':
                treefied=Phylotree.from_newick(tree)
                self.__trees[method]=treefied
            elif format=='json':
                treefied=Phylotree.from_json(tree)
                self.__trees[method]=treefied
            else:
                raise ValueError('Invalid format, please provide a valid format (nwk or json)')
        else:
            raise ValueError('Invalid tree type, please provide a valid tree (Phylotree, dict or str) and specify the format if it is a string')
        
        # -- when tree added successfully, add the family to the tree
        tree._add_family(self)

    def get_species_count(self):
        '''
        returns a dictionary of species distribution in the family
        '''
        species_dist = {}
        for member in self.__members:
            species_name = member.species.name
            if species_name in species_dist:
                species_dist[species_name] += 1
            else:
                species_dist[species_name] = 1
        return species_dist
    
    def distribution(self):
        '''
        returns a pandas dataframe of species distribution in the family
        '''
        species_dist = self.get_species_count()
        df = pd.DataFrame(species_dist.items(), columns=['Species', 'Count'])
        df['Label'] = df['Species'].apply(lambda x: f"Species: {x}")
        return df
    
    def plot_distribution(self):
        '''
        plots the species distribution in the family
        '''
        df=self.distribution()
        df.plot(kind='pie', x='Species', y='Count', title='Species distribution in family '+self.name, labels=df['Label'], autopct='%1.1f%%', legend=False)

    def _add_clan(self, clan):
        self.__clan=clan
        

    # -- static methods
    @staticmethod
    def get_instances():
        return Family.entries
    @staticmethod
    def get_family(id):
        for entry in Family.entries:
            if entry.id == id:
                return entry
        return None


    # -- generator function
    @staticmethod
    def from_rfam(query:str):
        i,n,t=get_family_attributes(query)
        tree_nwk=get_tree_newick_from_fam(i)
        tr=Phylotree.from_newick(tree_nwk)
        new_fam= Family(id=i, name=n, type=t,from_database=True)
        new_fam.add_tree(tr, method='rfam')
        return new_fam

if __name__=='__main__':

    # --testing
    fam1=Family.from_rfam('RF01510')
    fam2=Family.from_rfam('RF01511')
    fam3=Family.from_rfam('RF01512')

    # rna1= create_RNA_Molecule("7EAF")
    # fam1.add_RNA(rna1)

    print(fam1.trees['rfam'].family) #success



