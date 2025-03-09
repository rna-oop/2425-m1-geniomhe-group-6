# Lab 3 Report

## Table of contents

- [Lab 3 Report](#lab-3-report)
  - [Table of contents](#table-of-contents)
  - [First Implementation](#first-implementation)
    - [1. Parser returns a numpy array](#1-parser-returns-a-numpy-array)
    - [2. Writing Structures into PDML/XML format](#2-writing-structures-into-pdmlxml-format)
      - [i. Writer takes numpy array](#i-writer-takes-numpy-array)
      - [ii. Writer returns PDBML format](#ii-writer-returns-pdbml-format)
        - [file format description](#file-format-description)
        - [implementation: object to xml](#implementation-object-to-xml)
        - [implementation: ndarray to xml](#implementation-ndarray-to-xml)
      - [dev](#dev)

## First Implementation

### 1. Parser returns a numpy array

First, we kept our previous model and extended it with the minimal changes possible to have the functionality of the parser to return a numpy array. 

For this, we added a function in the `Processor` class called: `createArray()` that returns the required numpy array representation of an `RNA Molecule` that can have multiple models. 

Note: In our previous implementation, the parser will store the atom information in a list `atoms` inside the `Processor` class.

```python
def createArray(self):
        max_model_id=self.atoms[-1][-1] #access the model_id of the last atom 
        max_res_id=self.atoms[-1][6] #access the res_id of the last atom
        array=np.zeros((max_model_id+1, max_res_id+1, 3)) #initialize the array with zeros
        for atom in self.atoms: 
            model_id, res_id=atom[-1], atom[6] #access the model_id and res_id of the atom
            x, y, z = atom[1:4] #access the x,y,z coordinates of the atom
            array[model_id,res_id]=np.array([x,y,z]) #store the coordinates in the array
        return array
```
It returns a numpy array with the shape `(number of models, number of residues, 3)` where the last dimension represents the `x, y, z` coordinates of the atom. 

We added a boolean argument `array` to the `read()` function and set it to `True` by default. If the argument is `True`, the function will return the numpy array representation of the molecule, otherwise it will create the molecule object as before. We did not change anything in the `read()` function, we just added the following at the end:

```python
if array:
    return processor.createArray()
else:         
    return processor.createMolecule() 
```

We tested the implementation with the following code:

```python
rna_io=RNA_IO()
pdb_path_test=pathify_pdb("7eaf")
mol=rna_io.read(pdb_path_test, "PDB")
print(mol)
print("shape:", np.shape(mol))
```

The output was the following:

```
[[[ 0.0000e+00  0.0000e+00  0.0000e+00]
  [-1.0238e+01  5.7800e+00 -3.8326e+01]
  [-1.2861e+01  2.8200e+00 -4.0280e+01]
  [-1.4758e+01 -1.4300e-01 -4.0792e+01]
  [-1.5175e+01 -4.5880e+00 -4.1549e+01]
  [-1.5237e+01 -8.6290e+00 -4.0425e+01]
  [-1.2005e+01 -1.2462e+01 -3.6764e+01]
  [-1.3476e+01 -1.4405e+01 -3.4007e+01]
  [-1.4716e+01 -1.4456e+01 -2.9704e+01]
  [-1.1051e+01 -2.0912e+01 -2.5748e+01]
  [-6.7140e+00 -2.1716e+01 -2.4340e+01]
  [-3.9300e+00 -1.9415e+01 -2.2856e+01]
  [-7.0700e-01 -1.7054e+01 -2.0657e+01]
  .........
  [-9.3500e+00  2.7420e+00 -4.5980e+01]
  [-6.0820e+00  5.7550e+00 -4.4331e+01]]]
  shape: (1, 95, 3)
```

The output is a numpy array with the shape `(1, 95, 3)` which is the expected shape for the molecule `7eaf` that has 1 model and 94 residues.

### 2. Writing Structures into PDML/XML format

#### i. Writer takes numpy array

_tentative implementation_

recheck info stored in numpy array, should be of this form:

1 seq has 95 residues, **each residue having a list of atoms** (how is this represented, so far there are only 1 atom per residue?, should be a list of atoms), each atom has x,y,z coordinates.



#### ii. Writer returns PDBML format

##### file format description

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
> The atom_siteCategory tag is the only category that reflects teh information that we're capturing in this library, whether thorugh the RNA_Molecule object or the numpy array representation of it. This is the only category that will be included in the xml file. Others include information about bonds, symmetry, experimental setting and other metadata that is not captured in our object.

<!-- This is one atom entry in the file:

```xml
    <PDBx:atom_site id="1">
      <PDBx:B_iso_or_equiv>110.87</PDBx:B_iso_or_equiv>
      <PDBx:Cartn_x>-9.698</PDBx:Cartn_x>
      <PDBx:Cartn_y>3.426</PDBx:Cartn_y>
      <PDBx:Cartn_z>-31.854</PDBx:Cartn_z>
      <PDBx:auth_asym_id>A</PDBx:auth_asym_id>
      <PDBx:auth_atom_id>OP3</PDBx:auth_atom_id>
      <PDBx:auth_comp_id>G</PDBx:auth_comp_id>
      <PDBx:auth_seq_id>1</PDBx:auth_seq_id>
      <PDBx:group_PDB>ATOM</PDBx:group_PDB>
      <PDBx:label_alt_id xsi:nil="true"/>
      <PDBx:label_asym_id>A</PDBx:label_asym_id>
      <PDBx:label_atom_id>OP3</PDBx:label_atom_id>
      <PDBx:label_comp_id>G</PDBx:label_comp_id>
      <PDBx:label_entity_id>1</PDBx:label_entity_id>
      <PDBx:label_seq_id>1</PDBx:label_seq_id>
      <PDBx:occupancy>1.0</PDBx:occupancy>
      <PDBx:pdbx_PDB_model_num>1</PDBx:pdbx_PDB_model_num>
      <PDBx:type_symbol>O</PDBx:type_symbol>
    </PDBx:atom_site>
```  -->

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

##### implementation: object to xml

Luckily, _because our class implementation is well designed :)_, from an `RNA_Molecule` object, we are able to retrieve all information needed from an atom level. In other words, from each atom we can access to 1. which residue it belongs to 2. on which chain 3. of which model, besides the well defined attributes like coordinates, atom type, occupancy, etc.

In porcessor, this method takes an object and returns a lsit of atom dictionaries, where the keys of each dictionary are named exactly as the tags in the xml file. This way, we can easily create the xml file by iterating over the list of atoms and creating the corresponding tags.

```python
def extract_xml_atoms_from_rna(self, rna_molecule):
    atoms_list = []

    for model_num,_ in enumerate(rna_molecule.get_models()):  #--looping through all models 
        model=rna_molecule.get_models()[_] # --model object from dict key
    
        for chain in model.get_chains().values(): #--looping through all chains
            for residue in chain.get_residues().values(): #--looping through all residues  
                for atom_key, atom in residue.get_atoms().items(): #--looping through all atoms
                    atom_id, alt_id = atom_key  # unpacking atom key (alt_id is '' if no alt location)
                    # --keys defined identically to pdbml format, values extracted directly from atom object
                    atom_data = {
                        "id": str(len(atoms_list) + 1),  # Assign a sequential ID
                        "B_iso_or_equiv": str(atom.temp_factor),
                        "Cartn_x": str(atom.x),
                        "Cartn_y": str(atom.y),
                        "Cartn_z": str(atom.z),
                        "auth_asym_id": chain.id,
                        "auth_atom_id": atom_id,
                        "auth_comp_id": residue.type.name,
                        "auth_seq_id": str(residue.position),
                        "group_PDB": "ATOM", # assuming afor now that all are ATOM records
                        "label_alt_id": None if alt_id == "" else alt_id,
                        "label_asym_id": chain.id,
                        "label_atom_id": atom_id,
                        "label_comp_id": residue.type.name,
                        "label_entity_id": "1",  # should be one entity per xml for now
                        "label_seq_id": str(residue.position),
                        "occupancy": str(atom.occupancy),
                        "pdbx_PDB_model_num": model_num+1,
                        "type_symbol": atom.element.name
                    }

                    atoms_list.append(atom_data)
```

To convert to pdbml, xml library has been used, xml indettaion is handled by the `prettify_print_xml` decorator that uses teh `xml.dom.minidom` module. 

```python
# --helper function in processor module (not a method)
def pretty_print_xml(func):
    def wrapper(*args, **kwargs):
        xml_string = func(*args, **kwargs)
        xml_string = minidom.parseString(xml_string).toprettyxml(indent="    ")
        return xml_string
    return wrapper
```


and hierarchical xml structure is created by the `xml.etree.ElementTree` module.

```python
@pretty_print_xml
def create_xml_from_molecule(self,rna_molecule):
    root = ET.Element("PDBx:datablock", {
        "datablockName": rna_molecule.entry_id,
        "xmlns:PDBx": "http://pdbml.pdb.org/schema/pdbx-v50.xsd",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://pdbml.pdb.org/schema/pdbx-v50.xsd pdbx-v50.xsd"
    })

    atom_site_category = ET.SubElement(root, "PDBx:atom_siteCategory") #creates root with entry id
    atoms = self.extract_xml_atoms_from_rna(rna_molecule) # rna_molecule -> list of atom dictionaries

    for atom in atoms:
        atom_site = ET.SubElement(atom_site_category, "PDBx:atom_site", {"id": atom["id"]})

        for key, value in atom.items():
            if key == "id":
                continue
            element = ET.SubElement(atom_site, f"PDBx:{key}")
            if value is None:
                element.set("xsi:nil", "true")
            else:
                element.text = str(value) 

    xml_string = ET.tostring(root, encoding="unicode", method="xml")
    return xml_string
```

Eventually teh created xml string will be written into a file in `PDBML_Writer` class through a helper function

```python
def wrap_str_to_xml(s,name='pdbml_output.xml'):
    with open(name, "w") as f:
        f.write(s)
```

##### implementation: ndarray to xml

#### dev
_these are notes for dev purposes, to be removed later_

> [!CAUTION]
> the np array is currently of dimensions (no_models, no_atoms, 3) where the last dimension is the x,y,z coordinates of the atom. We need to change this to (no_models, no_residues, no_atoms, 3) making it 4dimensional (practically the first dim=1) because residue information is lost in the current implementation. Description states each row is an array of residues (this would allow proper indexing of residues). Respectively need to change the functions that were based on the old array structure in processor

> The issue arises when checking the pdb output, all atoms are by default belonging to one residue, souldn't seperate. Can take advantage of this issue to fix teh indexing of residues in the array, this way can seperate to chains too in processing. Assume one model and infer chains from the gaps between residues (even model num can be taken from first dim). (check the file viz on mol viewer, clearly shows different representation, line rep can not be dont since no residue type info is saved within the array)



- [x] added first implementation of PDBWriter to allow taking an np array
- [ ] fix the latter implementation ~after fixing array dimensions~
- [x] xml formatting and creation function added to processor (for rna mol) includes `atomSiteCategory` as the only category since no other info on bonds and symmetry is saved within our rna object
- [x] add PDML_Writer class
- [x] added xml and pdbl writing options in rna_io, tested with 7eaf (sample output in [demo.xml](./demo.xml))
- [ ] xml reader from array (temp implementation on the current array)

