from family import Family

class Clan:
    entries=[]

    def __init__(self, id, name=None, members=[]):
        ids = [clan.id for clan in Clan.entries]
        if id in ids:
            print('Clan with id already exists, linking to existing clan')
            existing_clan = Clan.get_clan(id)
            self.__dict__ = existing_clan.__dict__
        else:
            self.__id = id
            self.__name = name
            self.__members = members
            Clan.entries.append(self)
            print('Clan created successfully')

    def __validate_member(self, member):
        if not isinstance(member, Family):
            raise ValueError('Member must be an instance of Family')

    @staticmethod
    def get_instances():
        return Clan.entries
    @staticmethod
    def get_clan(id):
        for clan in Clan.entries:
            if clan.id==id:
                return clan
        return None
    
    @property
    def id(self):
        return self.__id
    @property
    def name(self):
        return self.__name
    @property
    def members(self):
        return self.__members
    @id.setter
    def id(self, value):
        raise ValueError('id is immutable')
    @name.setter
    def name(self, value):
        self.__name=value
    @members.setter
    def members(self, value):
        self.__members=value
    
    def __setattr__(self, name, value):
        if name == '_Clan__id':
            value=str(value)
            id_entries=[entry.id for entry in Clan.entries]
            if value in id_entries:
                print('Clan with this id already exists, will link it to the existing clan')
                self=Clan.get_clan(value)
            else:
                self.__dict__[name]=value
        elif name == '_Clan__name':
            value=str(value)
            self.__dict__[name]=value
        elif name=='_Clan__members':
            if not isinstance(value, list):
                raise ValueError('Members must be a list of Family objects')
            for member in value:
                self.__validate_member(member)
            self.__dict__[name]=value

    def __str__(self):
        clan=f'Clan {self.id}: {self.name}'
        members=f'\tMembers: {", ".join([member.name for member in self.members])}'
        return f'{clan}\n{members}'
    
    def __repr__(self):
        return f'''
        Clan(
            id={self.id}, 
            name={self.name}, 
            members={self.members}
        )'''

    def __eq__(self, other):
        if not isinstance(other, Clan):
            return NotImplemented
        return self.id == other.id
    

    def add_family(self, family):
        self.__validate_member(family)
        if family not in self.__members:
            self.__members.append(family)
        else:
            print('Family already in clan')

    def remove_family(self, family):
        if family in self.__members:
            self.__members.remove(family)
        else:
            print('Family not in clan')

if __name__=='__main__':
    f1=Family('f1', 'Family 1')
    f2=Family('f2', 'Family 2')
    f3=Family('f3', 'Family 3')
    c1=Clan('c1', 'Clan 1', [f1, f2])
    c2=Clan('c2', 'Clan 2', [f3])
    print(c1)
    print(c2)
    c1.add_family(f3)
    print('after adding f3:',c1)
    c1.remove_family(f2)
    print('after removing f2:',c1)