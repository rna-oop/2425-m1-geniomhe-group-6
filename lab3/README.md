# Lab 3 Report

## Table of contents

- [Lab 3 Report](#lab-3-report)
  - [Table of contents](#table-of-contents)
  - [First Implementation](#first-implementation)
    - [Class Diagram for the Previous-Model-Extension](#class-diagram-for-the-previous-model-extension)
    - [Object Diagram for the Previous-Model-Extension](#object-diagram-for-the-previous-model-extension)
    - [1. Parser returns a numpy array](#1-parser-returns-a-numpy-array)
    - [2. Writing Structures into PDML/XML format](#2-writing-structures-into-pdmlxml-format)

## First Implementation

**This implementation is in the branch `previous-model-extension `.**

In this lab, we extended our previous model to include the following functionalities:
- The parser returns a numpy array representation of the molecule.
- Writing structures into PDML/XML format.

### Class Diagram for the Previous-Model-Extension 

![Class-Diagram](model/Class-Diagram-Previous.jpg)

The new changes are highlighted in white.

### Object Diagram for the Previous-Model-Extension

![Object-Diagram](model/Object-Diagram-Previous.jpg)

### 1. Parser returns a numpy array

First, we kept our previous model and extended it with the minimal changes possible to have the functionality of the parser to return a numpy array. 

For this, we added a function in the `Processor` class called: `createArray()` that returns the required numpy array representation of an `RNA Molecule` that can have multiple models. 

Note: In our previous implementation, the parser will store the atom information in a list `atoms` inside the `Processor` class.

**createArray()** in `Processor` class:
- Returns a numpy array representation of the molecule
- Dimension: `(number of models, max_residues_no, max_atoms_per_residue_no, 3)` 
- Stores the x,y,z coordinates of each atom.
- Implementation notes:
  - To find the number of models we checked the model_id of the last atom in the atoms list. 
  - We had to loop through the list of atoms to find the maximum number of residues among all models and the maximum number of atoms per residue.
  - Considering that the same atom in a residue can have different coordinates (alternate locations), we stored the coordinates of the atom that has the highest occupancy.
  - The array is filled with nan values where there is no atom information.

**read() in `PDB_Parser` class:**
We added a boolean argument `array` to the `read()` function and set it to `True` by default. If the argument is `True`, the function will return the numpy array representation of the molecule, otherwise it will create the molecule object as before. We did not change anything in the `read()` function, we just added the following at the end:

```python
if array:
    return processor.createArray()
else:         
    return processor.createMolecule() 
```

**Code Usage**
An example can be found in the notebook [reading.ipynb](./demo/reading.ipynb). 
We read a molecule that contains 1 model and another molecule that contains multiple models, and showed the resulting arrays. 
A brief example:

```python
rna_io=RNA_IO()

pdb_path_test=pathify_pdb("7eaf")

mol=rna_io.read(pdb_path_test, "PDB")

print(mol.shape)
print(mol[0, -1, 0, :])
```

The output: 
```
(1, 94, 24, 3)
[-10.06    7.177 -49.234]
```

### 2. Writing Structures into PDML/XML format

**File format description:**

An PDBML file is an XML file that contains protein/nucleic acid structure information within an _xml format_. This is an efficient data storing format is widely used in databases and software tools to store and exchange data files in a structured manner. It was introduced to PDBe as the "PDBML" format by Westbrook et al. in a 2005 in a paper published in _Bioinformatics_ entitled "PDBML: the representation of archival macromolecular structure data in XML"[^1].

In python, writing and handling xml files is done here through 2 modules in our code: `xml.etree.ElementTree` and `xml.dom.minidom`. The first module is used to create the xml file and the second module is used to prettify the xml file (provide proper xml indentation).

Starting off by exploring this file (example used is 7eaf.xml taken from pdb), we notice the following structure

```xml
<PDBx:datablock xmlns:PDBx="http://pdbml.pdb.org/schema/pdbx-v50.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" datablockName="7EAF" xsi:schemaLocation="http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd">
  ...
</PDBx:datablock>
```

with all these tags included in the file:

```bash
grep -e '^   <PDBx:' 7eaf.xml #to retrive the list
```

- `<PDBx:atom_siteCategory>`
- `<PDBx:atom_site_anisotropCategory>`
- `<PDBx:atom_sitesCategory>`
- `<PDBx:atom_typeCategory>`
- `<PDBx:audit_authorCategory>`
- `<PDBx:audit_conformCategory>`
- `<PDBx:cellCategory>`
- `<PDBx:chem_compCategory>`
- `<PDBx:chem_comp_atomCategory>`
- `<PDBx:chem_comp_bondCategory>`
- `<PDBx:citationCategory>`
- `<PDBx:citation_authorCategory>`
- `<PDBx:database_2Category>`
- `<PDBx:diffrnCategory>`
- `<PDBx:diffrn_detectorCategory>`
- `<PDBx:diffrn_radiationCategory>`
- `<PDBx:diffrn_radiation_wavelengthCategory>`
- `<PDBx:diffrn_sourceCategory>`
- `<PDBx:entityCategory>`
- `<PDBx:entity_polyCategory>`
- `<PDBx:entity_poly_seqCategory>`
- `<PDBx:entryCategory>`
- `<PDBx:exptlCategory>`
- `<PDBx:exptl_crystalCategory>`
- `<PDBx:exptl_crystal_growCategory>`
- `<PDBx:ndb_struct_conf_naCategory>`
- `<PDBx:ndb_struct_na_base_pairCategory>`
- `<PDBx:ndb_struct_na_base_pair_stepCategory>`
- `<PDBx:pdbx_audit_revision_categoryCategory>`
- `<PDBx:pdbx_audit_revision_detailsCategory>`
- `<PDBx:pdbx_audit_revision_groupCategory>`
- `<PDBx:pdbx_audit_revision_historyCategory>`
- `<PDBx:pdbx_audit_revision_itemCategory>`
- `<PDBx:pdbx_audit_supportCategory>`
- `<PDBx:pdbx_database_statusCategory>`
- `<PDBx:pdbx_entity_nonpolyCategory>`
- `<PDBx:pdbx_entity_src_synCategory>`
- `<PDBx:pdbx_entry_detailsCategory>`
- `<PDBx:pdbx_initial_refinement_modelCategory>`
- `<PDBx:pdbx_nonpoly_schemeCategory>`
- `<PDBx:pdbx_poly_seq_schemeCategory>`
- `<PDBx:pdbx_refine_tlsCategory>`
- `<PDBx:pdbx_refine_tls_groupCategory>`
- `<PDBx:pdbx_struct_assemblyCategory>`
- `<PDBx:pdbx_struct_assembly_auth_evidenceCategory>`
- `<PDBx:pdbx_struct_assembly_genCategory>`
- `<PDBx:pdbx_struct_assembly_propCategory>`
- `<PDBx:pdbx_struct_conn_angleCategory>`
- `<PDBx:pdbx_struct_oper_listCategory>`
- `<PDBx:pdbx_struct_special_symmetryCategory>`
- `<PDBx:pdbx_validate_close_contactCategory>`
- `<PDBx:pdbx_validate_rmsd_bondCategory>`
- `<PDBx:refineCategory>`
- `<PDBx:refine_histCategory>`
- `<PDBx:refine_ls_restrCategory>`
- `<PDBx:refine_ls_shellCategory>`
- `<PDBx:reflnsCategory>`
- `<PDBx:reflns_shellCategory>`
- `<PDBx:softwareCategory>`
- `<PDBx:space_groupCategory>`
- `<PDBx:space_group_symopCategory>`
- `<PDBx:structCategory>`
- `<PDBx:struct_asymCategory>`
- `<PDBx:struct_connCategory>`
- `<PDBx:struct_conn_typeCategory>`
- `<PDBx:struct_keywordsCategory>`
- `<PDBx:struct_refCategory>`
- `<PDBx:struct_ref_seqCategory>`
- `<PDBx:symmetryCategory>`

[^1]:PDBML: the representation of archival macromolecular structure data in XML.
Westbrook J, Ito N, Nakamura H, Henrick K, Berman HM.
Bioinformatics, 2005, 21(7):988-992. PubMed:15509603 full text

The `<PDBx:atom_siteCategory>` tag contains all the information about the atoms in the structure, including all the hierarchical information model > chain > residue > atom. Thus the structure is solely defined by a list of atoms, in this format each will be represented by a tag `<PDBx:atom_site>`. 

```xml
<PDBx:datablock xmlns:PDBx="http://pdbml.pdb.org/schema/pdbx-v50.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" datablockName="7EAF" xsi:schemaLocation="http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd">
  <PDBx:atom_siteCategory>
    <PDBx:atom_site id="1">
    ...
    </PDBx:atom_site>
    <PDBx:atom_site id="2">
    ...
  </PDBx:atom_siteCategory>
</PDBx:datablock>
```

> [!IMPORTANT]
> The atom_siteCategory tag is the only category that reflects the information that we're capturing in this library, whether thorugh the RNA_Molecule object or the numpy array representation of it. This is the only category that will be included in the xml file. Others include information about bonds, symmetry, experimental setting and other metadata that is not captured in our object.

This is how the hierarchy leading to an atom representation is portrayed in the `.xml` file.

```
PDBx:datablock
├── datablockName
├── xsi:schemaLocation
└── PDBx:atom_siteCategory
    └── PDBx:atom_site
        ├── id
        ├── PDBx:B_iso_or_equiv
        ├── PDBx:Cartn_x
        ├── PDBx:Cartn_y
        ├── PDBx:Cartn_z
        ├── PDBx:auth_asym_id
        ├── PDBx:auth_atom_id
        ├── PDBx:auth_comp_id
        ├── PDBx:auth_seq_id
        ├── PDBx:group_PDB
        ├── PDBx:label_alt_id
        ├── PDBx:label_asym_id
        ├── PDBx:label_atom_id
        ├── PDBx:label_comp_id
        ├── PDBx:label_entity_id
        ├── PDBx:label_seq_id
        ├── PDBx:occupancy
        ├── PDBx:pdbx_PDB_model_num
        └── PDBx:type_symbol
```



Notice a slight difference between the representation of an atom with $occupancy=1$ and an atom with $occupancy<1$ (having an altrnate location). The difference is the presence of the `label_alt_id` tag. This will be taken care of while writing the file. This being said, each alternative location of an atom is cosidered a different atom in the file (with `PDBx:atom_site id` being $+1$ the id of the previous alternate location).

<table>
  <tr>
    <th>Atom with no alternative location</th>
    <th>Atom with alternative location</th>
  </tr>
  <tr>
    <td>
      <pre><code>&lt;PDBx:atom_site id="1"&gt;
  &lt;PDBx:B_iso_or_equiv&gt;110.87&lt;/PDBx:B_iso_or_equiv&gt;
  &lt;PDBx:Cartn_x&gt;-9.698&lt;/PDBx:Cartn_x&gt;
  &lt;PDBx:Cartn_y&gt;3.426&lt;/PDBx:Cartn_y&gt;
  &lt;PDBx:Cartn_z&gt;-31.854&lt;/PDBx:Cartn_z&gt;
  &lt;PDBx:auth_asym_id&gt;A&lt;/PDBx:auth_asym_id&gt;
  &lt;PDBx:auth_atom_id&gt;OP3&lt;/PDBx:auth_atom_id&gt;
  &lt;PDBx:auth_comp_id&gt;G&lt;/PDBx:auth_comp_id&gt;
  &lt;PDBx:auth_seq_id&gt;1&lt;/PDBx:auth_seq_id&gt;
  &lt;PDBx:group_PDB&gt;ATOM&lt;/PDBx:group_PDB&gt;
  &lt;PDBx:label_alt_id xsi:nil="true"/&gt;
  &lt;PDBx:label_asym_id&gt;A&lt;/PDBx:label_asym_id&gt;
  &lt;PDBx:label_atom_id&gt;OP3&lt;/PDBx:label_atom_id&gt;
  &lt;PDBx:label_comp_id&gt;G&lt;/PDBx:label_comp_id&gt;
  &lt;PDBx:label_entity_id&gt;1&lt;/PDBx:label_entity_id&gt;
  &lt;PDBx:label_seq_id&gt;1&lt;/PDBx:label_seq_id&gt;
  &lt;PDBx:occupancy&gt;1.0&lt;/PDBx:occupancy&gt;
  &lt;PDBx:pdbx_PDB_model_num&gt;1&lt;/PDBx:pdbx_PDB_model_num&gt;
  &lt;PDBx:type_symbol&gt;O&lt;/PDBx:type_symbol&gt;
&lt;/PDBx:atom_site&gt;
</code></pre>
    </td>
    <td>
      <pre><code>&lt;PDBx:atom_site id="170"&gt;
  &lt;PDBx:B_iso_or_equiv&gt;66.5&lt;/PDBx:B_iso_or_equiv&gt;
  &lt;PDBx:Cartn_x&gt;-14.543&lt;/PDBx:Cartn_x&gt;
  &lt;PDBx:Cartn_y&gt;-18.821&lt;/PDBx:Cartn_y&gt;
  &lt;PDBx:Cartn_z&gt;-25.673&lt;/PDBx:Cartn_z&gt;
  &lt;PDBx:auth_asym_id&gt;A&lt;/PDBx:auth_asym_id&gt;
  &lt;PDBx:auth_atom_id&gt;P&lt;/PDBx:auth_atom_id&gt;
  &lt;PDBx:auth_comp_id&gt;A&lt;/PDBx:auth_comp_id&gt;
  &lt;PDBx:auth_seq_id&gt;9&lt;/PDBx:auth_seq_id&gt;
  &lt;PDBx:group_PDB&gt;ATOM&lt;/PDBx:group_PDB&gt;
  &lt;PDBx:label_alt_id&gt;A&lt;/PDBx:label_alt_id&gt;
  &lt;PDBx:label_asym_id&gt;A&lt;/PDBx:label_asym_id&gt;
  &lt;PDBx:label_atom_id&gt;P&lt;/PDBx:label_atom_id&gt;
  &lt;PDBx:label_comp_id&gt;A&lt;/PDBx:label_comp_id&gt;
  &lt;PDBx:label_entity_id&gt;1&lt;/PDBx:label_entity_id&gt;
  &lt;PDBx:label_seq_id&gt;9&lt;/PDBx:label_seq_id&gt;
  &lt;PDBx:occupancy&gt;0.44&lt;/PDBx:occupancy&gt;
  &lt;PDBx:pdbx_PDB_model_num&gt;1&lt;/PDBx:pdbx_PDB_model_num&gt;
  &lt;PDBx:type_symbol&gt;P&lt;/PDBx:type_symbol&gt;
&lt;/PDBx:atom_site&gt;
</code></pre>
    </td>
  </tr>
</table>

_in this example id 171 is alt location B of the same atom in 170, and shows different occupancy_

**Implementation: object to xml**

Thanks to the hierarchical class design of the molecule object, we're able to retrieve all information needed describing an atom, for each atom in the molecule.

In porcessor, this method `flattenMolecule_to_dict` takes an object and returns a list of atom dictionaries, where the keys of each dictionary are named exactly as the tags in the xml file. This way, we can easily create the xml file by iterating over the list of atoms and creating the corresponding tags.

```python
    def flattenMolecule_to_dict(self,rna_molecule:RNA_Molecule):
        '''
        rna_molecule: RNA_Molecule object -> RNA molecule to be flattened -> list of atom dictionaries
        '''
        atoms_list = []

        for model_num,_ in enumerate(rna_molecule.get_models()):  #--looping through all models 
            model=rna_molecule.get_models()[_] # --model object from dict key
            
            for chain in model.get_chains().values(): #--looping through all chains
                for residue in chain.get_residues().values(): #--looping through all residues  
                    for atom_key, atom in residue.get_atoms().items(): #--looping through all atoms
                        atom_id, alt_id = atom_key  # unpacking atom key (alt_id is '' if no alt location)
                        # --keys defined identically to pdbml format, values extracted directly from atom object
                        atom_data = {
                            "atom_id": str(len(atoms_list) + 1),  # Assign a sequential ID
                            "B": str(atom.temp_factor),
                            "x": str(atom.x),
                            "y": str(atom.y),
                            "z": str(atom.z),
                            "chain_id": chain.id,
                            "atom_id": atom_id,
                            "residue_type": residue.type.name,
                            "residue_pos": str(residue.position),
                            "alt_id": None if alt_id == "" else alt_id,
                            "occupancy": str(atom.occupancy),
                            "model_no": model_num+1,
                            "atom_element": atom.element.name
                        }
                        atoms_list.append(atom_data)
        return atoms_list
```

To convert to PDBML, xml formatting private functions have been implemented in `PDBML_Writer` submodule. 

```python
# --helper methods
    def _wrap_str_to_xml(self,s,name='pdbml_output.xml'):
        with open(name, "w") as f:
            f.write(s)

    def _format_atom_info(self, atoms_list,entry_id):
        '''
        formats a list of atoms dicts into XML format
        '''
        s='''<?xml version="1.0" encoding="UTF-8" ?>
<PDBx:datablock datablockName="'''+entry_id+'''"
   xmlns:PDBx="http://pdbml.pdb.org/schema/pdbx-v50.xsd"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd">'''
        s+='\n\t<PDBx:atom_siteCategory>\n'
        for atom in atoms_list:
            s+='\t\t<PDBx:atom_site id="'+atom["atom_id"]+'">\n'
            s+='\t\t\t<PDBx:B_iso_or_equiv>'+str(atom['B'])+'</PDBx:B_iso_or_equiv>\n'
            s+='\t\t\t<PDBx:Cartn_x>'+str(atom['x'])+'</PDBx:Cartn_x>\n'
            s+='\t\t\t<PDBx:Cartn_y>'+str(atom['y'])+'</PDBx:Cartn_y>\n'
            s+='\t\t\t<PDBx:Cartn_z>'+str(atom['z'])+'</PDBx:Cartn_z>\n'
            s+='\t\t\t<PDBx:auth_asym_id>'+atom['chain_id']+'</PDBx:auth_asym_id>\n'
            s+='\t\t\t<PDBx:auth_atom_id>'+atom['atom_id']+'</PDBx:auth_atom_id>\n'
            s+='\t\t\t<PDBx:auth_comp_id>'+atom['residue_type']+'</PDBx:auth_comp_id>\n'
            s+='\t\t\t<PDBx:auth_seq_id>'+str(atom['residue_pos'])+'</PDBx:auth_seq_id>\n'
            s+='\t\t\t<PDBx:group_PDB>ATOM</PDBx:group_PDB>\n'
            if atom['alt_id'] is not None:
                s+='\t\t\t<PDBx:label_alt_id xsi:nil="true" />\n'
            else:
                atom['alt_id']='A'
            s+='\t\t\t<PDBx:label_asym_id>'+atom['alt_id']+'</PDBx:label_asym_id>\n'
            s+='\t\t\t<PDBx:label_atom_id>'+atom['atom_id']+'</PDBx:label_atom_id>\n'
            s+='\t\t\t<PDBx:label_comp_id>'+atom['residue_type']+'</PDBx:label_comp_id>\n'
            s+='\t\t\t<PDBx:label_entity_id>1</PDBx:label_entity_id>\n'
            s+='\t\t\t<PDBx:label_seq_id>'+str(atom['residue_pos'])+'</PDBx:label_seq_id>\n'
            s+='\t\t\t<PDBx:occupancy>'+str(atom['occupancy'])+'</PDBx:occupancy>\n'
            s+='\t\t\t<PDBx:pdbx_PDB_model_num>'+str(atom['model_no'])+'</PDBx:pdbx_PDB_model_num>\n'
            s+='\t\t\t<PDBx:type_symbol>'+atom['atom_element']+'</PDBx:type_symbol>\n'
            s+='\t\t</PDBx:atom_site>\n'
        s+='\t</PDBx:atom_siteCategory>\n'
        s+='</PDBx:datablock>'
        return s
```

**Code usage:**

```python
mol: RNA_Molecule #suppose a declared instance of RNA_Molecule

rna_io=RNA_IO()
rna_io.write(mol, "7eaf_object.xml",'PDBML')
```

_example output:_

```bash
cat 7eaf_object.xml
```

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<PDBx:datablock datablockName="7EAF"
   xmlns:PDBx="http://pdbml.pdb.org/schema/pdbx-v50.xsd"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd">
	<PDBx:atom_siteCategory>
		<PDBx:atom_site id="OP3">
			<PDBx:B_iso_or_equiv>110.87</PDBx:B_iso_or_equiv>
			<PDBx:Cartn_x>-9.698</PDBx:Cartn_x>
			<PDBx:Cartn_y>3.426</PDBx:Cartn_y>
			<PDBx:Cartn_z>-31.854</PDBx:Cartn_z>
			<PDBx:auth_asym_id>A</PDBx:auth_asym_id>
			<PDBx:auth_atom_id>OP3</PDBx:auth_atom_id>
			<PDBx:auth_comp_id>G</PDBx:auth_comp_id>
			<PDBx:auth_seq_id>1</PDBx:auth_seq_id>
			<PDBx:group_PDB>ATOM</PDBx:group_PDB>
			<PDBx:label_asym_id>A</PDBx:label_asym_id>
			<PDBx:label_atom_id>OP3</PDBx:label_atom_id>
			<PDBx:label_comp_id>G</PDBx:label_comp_id>
			<PDBx:label_entity_id>1</PDBx:label_entity_id>
			<PDBx:label_seq_id>1</PDBx:label_seq_id>
			<PDBx:occupancy>1.0</PDBx:occupancy>
			<PDBx:pdbx_PDB_model_num>1</PDBx:pdbx_PDB_model_num>
			<PDBx:type_symbol>O</PDBx:type_symbol>
		</PDBx:atom_site>
...
```

a minor addition to `RNA_IO` class was made to include the option of writing in PDBML format. 

```python
class RNA_IO:
    def __init__(self):
        ...
        self.__writers={"PDB": PDB_Writer(),'PDBML': PDBML_Writer(),'XML': PDBML_Writer()}
```



**Parallelism with PDB_Writer**

- [x] user interface:
```python
rna_io=RNA_IO()
mol: RNA_Molecule 

rna_io.write(mol, "7eaf_object.xml",'PDBML') #also works by specifying XML
rna_io.write(mol, "7eaf_object.pdb",'PDB')
```


| PDB_Writer | PDBML_Writer |
|------------|--------------|
| inherits RNA_Writer abstract class | inherits RNA_Writer abstract class |
| `write(molecule: RNA_Molecule, file_path: str)` | `write(molecule: RNA_Molecule, file_path: str) |
| takes an RNA_Molecule object | takes an RNA_Molecule object |
| uses processor instance to get the atom information | uses processor instance to get the atom information |
| uses processor.flattenMolecule() | uses processor.flattenMolecule_to_dict() |
| has format specific private method `_format_atom_info()` and `_format_molecule_info` | has format specific private method `_format_atom_info()` and `_wrap_str_to_xml()` |
| writes the pdb file | writes the pdbml file |

<!-- 
#### dev
_these are notes for dev purposes, to be removed later_

> [!CAUTION]
> the np array is currently of dimensions (no_models, no_atoms, 3) where the last dimension is the x,y,z coordinates of the atom. We need to change this to (no_models, no_residues, no_atoms, 3) making it 4dimensional (practically the first dim=1) because residue information is lost in the current implementation. Description states each row is an array of residues (this would allow proper indexing of residues). Respectively need to change the functions that were based on the old array structure in processor

> The issue arises when checking the pdb output, all atoms are by default belonging to one residue, souldn't seperate. Can take advantage of this issue to fix the indexing of residues in the array, this way can seperate to chains too in processing. Assume one model and infer chains from the gaps between residues (even model num can be taken from first dim). (check the file viz on mol viewer, clearly shows different representation, line rep can not be dont since no residue type info is saved within the array)



- [x] added first implementation of PDBWriter to allow taking an np array
- [ ] fix the latter implementation ~after fixing array dimensions~
- [x] xml formatting and creation function added to processor (for rna mol) includes `atomSiteCategory` as the only category since no other info on bonds and symmetry is saved within our rna object
- [x] add PDML_Writer class
- [x] added xml and pdbl writing options in rna_io, tested with 7eaf (sample output in [demo.xml](./demo.xml))
- [ ] xml reader from array (temp implementation on the current array)
 -->
