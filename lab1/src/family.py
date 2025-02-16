from RNA_Molecule import RNA_Molecule

from utils import get_family_attributes, create_RNA_Molecule, get_tree_newick_from_fam
from tree import Phylotree


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

    This class has the following methods:

    - helper methods:
        - __validate_member(member): validate if the member is an instance of RNA_Molecule
        - __delete_family(id): delete the family with the given id from the entries list

    - instance methods:
        - `add_RNA(self, RNA)`
        - `remove_RNA(self, RNA)`


    - class methods:
        - `get_instances()`
        - `get_family(id)`
        - `reset()` (delete all instances, used with caution)

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

    def __init__(self, id, name, type=None, members=[], tree=None, from_database=False):
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
            self.__tree = tree

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
    def tree(self):
        return self.__tree
    @tree.setter
    def tree(self, value):
        self.__tree = value

    # --dunders
    def __eq__(self, other):
        return self.id == other.id

    # def __del__(self):
    #     Family.__delete_family(self.id)
    #     print('Family deleted')

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
        elif name=='_Family__tree':
            if isinstance(value, Phylotree):
                super().__setattr__(name, value)
            elif value is None:
                super().__setattr__(name, value)
            else:
                raise ValueError('Tree must be an instance of Phylotree')


    def __str__(self):
        fam='-- Family: '+self.name+' ('+self.id+')\n'
        if self.type:
            fam+='\tType: '+self.type+'\n'
        if self.members != []:
            fam+='\tMembers:\n'
            for member in self.members:
                fam+='\t\t'+str(member)+'\n'
        if self.tree:
            fam+='------------------------------------------------------------------------------------\n\t\t\t\tTree:\n'+str(self.tree)
        return fam

    def __repr__(self):
        return f'''
        Family(
            id={self.id}, 
            name={self.name}, 
            type={self.type}, 
            members={self.members},
            tree={self.tree}
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

    # @staticmethod
    # def reset():
    #     while Family.entries:  
    #         entry = Family.entries.pop() 
    #         del entry  


    # -- generator function
    @staticmethod
    def from_rfam(query:str):
        i,n,t=get_family_attributes(query)
        tree_nwk=get_tree_newick_from_fam(i)
        tr=Phylotree.from_newick(tree_nwk)
        return Family(id=i, name=n, type=t, tree=tr,from_database=True)

if __name__=='__main__':

    # --testing
    fam1=Family.from_rfam('SAM')
    rna1= create_RNA_Molecule("7EAF")
    fam1.add_RNA(rna1)
    print(fam1) #success

