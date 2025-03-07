# Lab 3 Report

## Table of contents

- [Lab 3 Report](#lab-3-report)
  - [Table of contents](#table-of-contents)
  - [First Implementation](#first-implementation)
    - [1. Parser returns a numpy array](#1-parser-returns-a-numpy-array)
  

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

