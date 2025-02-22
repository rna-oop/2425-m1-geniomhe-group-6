'''
species module: contains class Species
'''

from family import Family

class Species:
    '''
    type Species:

    > Species refer to the organisms (bacteria, animals, plants, etc.) that contain RNA sequences belonging to a particular RNA family
    
    In this class, a species is defined solely by its name. Optionally, it can be defined by its species, genus, family, order, class, phylum, kingdom, and domain.
    All species instances are stored in the declared_species list class attribute to make sure no species is declared twice (equality is based on the name attribute) !!!

    Most important attributes:

    - declared_species [CLASS ATTRIBUTE]: list, contains all the species instances declared so far to avoid duplicates (this allows saving information about a species set of families without isntanciating a family everytime)

    - name: str, name of the species (key attribute, has to b unique for each species, can be named by accession of a sp if needed)
    - families: list, this attribute represents the many to many relationship between species and families, it is a list of Family instances that contain the species

    Everytime we add a species to a family, we also add the family to the species instance, this is done in the _add_family method implicitly from the family module (user should not worry about this; this is why it's a private method)

    helper methods:
    - _get_species: static method, takes a name and returns the species instance with that name if it exists, otherwise returns None (to allow singleton instances with the same name)
    - _add_family: method, takes a family instance and adds it to the species instance, this is done when adding a new species from the Family class

    *validation is handeled for family object, otherwise warning is printed*
    '''
    declared_species = [] #addition will be in setattr after making sure the name is unique

    def __init__(self, name, species=None, genus=None, family=None, order=None, class_=None, phylum=None, kingdom=None, domain=None):
        names=[species.name for species in Species.declared_species]
        if name in names:
            print('Species with this name already exists, will return the same instance')
            existing_species = Species._get_species(name)
            self.__dict__ = existing_species.__dict__
                    
        else:      
            self.__name = name
            self.__families=[]

            # self.__species = species
            # self.__genus = genus
            # self.__family = family
            # self.__order = order
            # self.__class_ = class_
            # self.__phylum = phylum
            # self.__kingdom = kingdom
            # self.__domain = domain

    def __setattr__(self, name, value):
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
    @property
    def families(self):
        return self
    # @property
    # def species(self):
    #     return self.__species
    # @property
    # def genus(self):
    #     return self.__genus
    # @property
    # def family(self):
    #     return self.__family
    # @property
    # def order(self):
    #     return self.__order
    # @property
    # def class_(self):
    #     return self.__class_
    # @property
    # def phylum(self):
    #     return self.__phylum
    # @property
    # def kingdom(self):
    #     return self.__kingdom
    # @property
    # def domain(self):
    #     return self.__domain
    
    @name.setter
    def name(self, value):
        print('Warning: name is immutable, cannot be changed; taken as key of an instance, considering deleting the instance and creating a new one')
    @families.setter
    def families(self, value):
        print('Warning: can not change families already added to the species, will lose all information')
    # @species.setter
    # def species(self, value):
    #     self.__species = value
    # @genus.setter
    # def genus(self, value):
    #     self.__genus = value
    # @family.setter
    # def family(self, value):
    #     self.__family = value
    # @order.setter
    # def order(self, value):
    #     self.__order = value
    # @class_.setter
    # def class_(self, value):
    #     self.__class_ = value
    # @phylum.setter
    # def phylum(self, value):
    #     self.__phylum = value
    # @kingdom.setter 
    # def kingdom(self, value):
    #     self.__kingdom = value
    # @domain.setter
    # def domain(self, value):
    #     self.__domain = value
    
    def __str__(self):
        s=f"Species: {self.__name}"
        if self.__families:
            s+=f"\n\tFamilies:"
            for family in self.__families:
                s+=f'\n\t\t-- Family: \n{family}\n'
        # if self.__domain:
        #     s+=f"\n\tDomain: {self.__domain}"
        # if self.__kingdom:
        #     s+=f"\n\tKingdom: {self.__kingdom}"
        # if self.__phylum:
        #     s+=f"\n\tPhylum: {self.__phylum}"
        # if self.__class_:
        #     s+=f"\n\tClass: {self.__class_}"
        # if self.__order:
        #     s+=f"\n\tOrder: {self.__order}"
        # if self.__family:
        #     s+=f"\n\tFamily: {self.__family}"
        # if self.__genus:
        #     s+=f"\n\tGenus: {self.__genus}"
        # if self.__species:
        #     s+=f"\n\tSpecies: {self.__species}"
        return s

    @staticmethod
    def _get_species(name):
        for species in Species.declared_species:
            if species.name == name:
                return species
        return None  

    def _add_family(self, family):
        '''
        helper function to add a family to the species object when it is used in the family module

        we dont want to add species to family as well since this will create  a recursive loop, 
        the user must always add a species from a family instance and addition to the species instance will be done automatically
        '''
        if not isinstance(family, Family):
            print('Warning: Not a Family instance')
            return
        if family not in self.__families:
            self.__families.append(family)
        print(f'Family {family.name} already exists in the species {self.__name}; not added again')
      
    def __repr__(self):
        return f'''
        Species(
            name={self.__name},
            families={self.__families}
        )'''
    
    def __eq__(self, other):
        if not isinstance(other, Species):
            print('Warining: Not the same Species type')
            return False
        return self.__name == other.name
    


if __name__ == '__main__':
    s1=Species('H')
    print(s1)
    s2=Species('a', species='jok')
    print(s2)
    s3=Species('H', species='jok') #same name as s1 shdoule be same instance
    print(s3)
    print(s1==s3) #success