import json,os
from utils import * #to parse newick string

class TreeNode:
    '''
    *helper Tree Node class for Phylogenetic Tree*

    Building blocks of the nodes list attribute in Pylotree to store node information of the graph data structure
    Hold RNA type as the data attribute and a list of children nodes
    
    Important notes on attributes:  
    
    - branch_lengtth as an attribute to store the distance between the node and its parent
    - parent attribute to store the parent node of the current node
    - children attribute to store the children nodes of the current node

    methods:

    - add_child(child, weight): add a child node to the current node with a given weight (distance, no longer useful since added branch_length as an attribute)
    - preorder_traversal(level=0): traverse the tree in preorder and return a string representation of the tree

    + dunder methods:
        - __repr__: representation of the node
        - __str__: string representation of the node
        - __getitem__: get a child node by name
    
    '''
    def __init__(self, name=None, branch_length=None, parent=None):
        self.name = name
        self.branch_length = branch_length
        self.parent = parent
        self.children = {}

    def add_child(self, child, weight):
        child.parent = self
        self.children[child] = weight
    
    def __repr__(self):
        return f"Node {self.name if self.name else 'Internal'}: {self.branch_length}"
    
    def __str__(self):
        return str(self.name if self.name else 'Internal')

    def __getitem__(self, child_name):
        child_str = str(child_name)
        for child in self.children.keys():
            if str(child) == child_str:
                print(f'Child {child_str} of {self} found at distance {self.children[child]}')
                return child
        raise KeyError(f"Node {child_name} not found in children of {self}")
    
    def preorder_traversal(self, level=0):
        indent = "  " * level
        result = f"{indent}- {self.name if self.name else 'Internal'} (Branch Length: {self.branch_length})\n"
        for child in self.children.keys():
            result += child.preorder_traversal(level + 1)
        return result





class Phylotree:
    '''
    Phylogenetic Tree 
    -----------------------------------

    A class to represent a phylogenetic tree for RNA sequences:
    > "A phylogenetic tree represents the evolutionary relationships between RNA sequences in a given RNA family.
    It  is  constructed  using  multiple  sequence  alignments  and  computational  phylogenetics  to  illustrate  how
    different  RNA  sequences  are  related  through  common  ancestry.  These  trees  help  in  understanding  RNA
    structure conservation, functional similarities, and evolutionary divergence within RNA families. 
    You can take alook  at  the  phylogenetic  tree  of  the  SAM  riboswitch  Rfam  family,  which  includes  the  RNA structure  7EAF
    discussed earlier, here: https://rfam.org/family/SAM#tabview=tab5."

    This will be implemented as a tree data structure, with a root node as attribute

    Conceptually:

    - internal nodes represent hypothetical common ancestral sequences  
    - leaf nodes represent RNA sequences in the family, which will be of type RNA-

    The string representation will be a preorder traversal of the tree, running from the root

    '''

    def __init__(self, from_generator=False):
        '''
        Constructor, takes attributes:

        from_generator: bool
            > If True, the tree will be built from a generator (not normal initialization) 
            It's used to warn the user that inisitalizating the tree directly as Phylotree() will not build the tree, it'll be empty and requires adding entries to it manually
            Recommended usage (non developer): Phylotree.from_newick(...) which will call this constructor with from_generator=True
        
        _e.g.,_
        ```python
        >>> tree = Phylotree()
        Warning: Initializing Phylotree directly will not build the tree, it'll be empty and requires adding entries to it manually
        >>> tree = Phylotree.from_newick("((A:0.1,B:0.2):0.3,C:0.4);") #uses a static generator method to build the tree 
        '''
        self.__root=None
        if not from_generator:
            print("Warning: Initializing Phylotree directly will not build the tree, it'll be empty and requires adding entries to it manually")

        
    @property
    def root(self):
        return self.__root
    @root.setter
    def root(self, node):
        self.__root = node

        
    @staticmethod
    def build_tree(tree_dict, parent=None):
        '''
        helper method to build the tree from a dictionary
        returns the root node of the tree

        params:
        - tree_dict: dict  
            dictionary representation of the tree
        - parent: TreeNode  
            parent node of the current node

        returns:
        - node: TreeNode, root node of the tree

        note for later: check why when making the method private it's giving error
        '''
        node_name = tree_dict.get("name", None)
        branch_length = tree_dict.get("branch_length", None)
        node = TreeNode(name=node_name, branch_length=branch_length, parent=parent)
        
        for child in tree_dict.get("children", []):
            child_node = Phylotree.build_tree(child, parent=node)
            node.add_child(child_node, child_node.branch_length)
        
        return node

    @staticmethod
    def from_dict(tree_dict, parent=None):
        root_node = Phylotree.build_tree(tree_dict, parent)
        tree = Phylotree(from_generator=True)
        tree.root = root_node
        return tree
    
    @staticmethod
    def from_json(json_str):
        # check if path transform
        if json_str.endswith('.json') and os.path.exists(json_str):
            with open(json_str, 'r') as f:
                json_str = f.read()
        tree_dict = json.loads(json_str)
        return Phylotree.from_dict(tree_dict)
    
    @staticmethod
    def from_newick(newick_str):
        '''
        provided a newick file or string, parse it and build the tree

        params:
        - newick_str: str (or path),
            newick string or path to a newick file
        
        returns:
        - tree: Phylotree,  
            the built phylogenetic
        '''
        if os.path.exists(newick_str):
            with open(newick_str, 'r') as f:
                newick_str = f.read()

        tree_json = parse_newick(newick_str)
        json_output = json.dumps(tree_json, indent=2)
        tree=Phylotree.from_json(json_output) 
        return tree

    
    def __str__(self):
        return self.root.preorder_traversal()
    
    def __repr__(self):
        return self.__str__()+"\n"+f'Root: {self.root}'

if __name__=='__main__':
    tree_dict={
        "children": [
            {
            "name": "a",
            "branch_length": 0.05592
            },
            {
            "name": "b",
            "branch_length": 0.08277
            },
            {
            "children": [
                {
                "name": "c",
                "branch_length": 0.11049
                },
                {
                "name": "d",
                "branch_length": 0.31409
                }
            ],
            "branch_length": 0.340
            }
        ],
        "branch_length": 0.03601
    }
    tree=Phylotree.from_dict(tree_dict) #success
    # tree=Phylotree.from_json('test/tree.json') #success
    newick_str = '''
    (87.4_AE017263.1/29965-30028_Mesoplasma_florum_L1[265311].1:0.05592,
    _URS000080DE91_2151/1-68_Mesoplasma_florum[2151].1:0.08277,
        (90_AE017263.1/668937-668875_Mesoplasma_florum_L1[265311].2:0.11049,
        81.3_AE017263.1/31976-32038_Mesoplasma_florum_L1[265311].3:0.31409)
    0.340:0.03601);
    '''
    tree=Phylotree.from_newick(newick_str) #success  
    # tree=Phylotree.from_newick('lab1/examples/RF00162.nhx')  #success
    
    print(tree)

