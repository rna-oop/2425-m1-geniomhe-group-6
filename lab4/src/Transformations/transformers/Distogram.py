import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.BaseTransformer import BaseTransformer

import numpy as np

class Distogram(BaseTransformer):
    '''
    class Distogram

    This class is used to transform the input data into a distogram representation

    *Whats a distogram?*  
    A distogram is a representation of the distances between pairs of residues in a structure

    This class inherits from teh abstract class BaseTransformer and implements the abstract method transform
    The transformation is particularly applied to the output of the model y, which is a 3D array of coordinates

    usage:
    ```
    >>> from Transformations.transformers.Distogram import Distogram
    >>> X,y = Distogram().transform(X, Y, atoms=[1,3,5], b=5)
    ```
    
    '''
    def __init__(self):
        pass

    def transform(self, X, Y, atoms=1, b=None):
        '''
        `Distogram().transform(X,Y)`: Distogram's transform method, Computing a distogram from the coordinates of the atoms in the RNA structure  

        parameters:

        - X: np.ndarray, sequence data | mandatory
        - Y: np.ndarray or dict, dict containing Original item that is nparray -> coordinates data (3D coordinates of atoms) | mandatory
        - atoms: list or int (optional), list of atom indices (or 1 atom index) to be used for distogram calculation (default set to 1st atom in 5'-3' direction)
        - b: int (optional), number of buckets for discretization (if None, no bucketing is performed)

        returns:
        - X: np.ndarray, sequence data (unchanged)
        - Y_transformed: np.ndarray, distogram data

        :description:  
        - distogram is a 2d matrix showing residues x residues matrix of distances
        - each structure in y is transformed into a distogram (number of structures in y <=> nrows in y <=> number of distograms)
        - all distograms will be concatenated in a single ndarray suc that nrows in y_transformed = nrows in y
        - distogram is of shape (L x L x k) where L is the number of residues and k is the number of atoms used (3D matrix showing residues x residues x atoms given)
        - if k=1, distogram is of shape (L x L)
        - if b is given, i.e. user wants to split distances in b buckets, distogram is of shape (L x L x k x b) or (L x L x b) if k=1

        *whats bucketing?*
        > bucketing is a process of splitting the distances into b buckets (or bins) to create a histogram-like representation of the distances
        > for example, if the maximum distance is 10 and b=5, the distances will be split into 5 buckets of size 2 (0-2, 2-4, 4-6, 6-8, 8-10)
        > if a distance falls into a bucket, the corresponding bucket in the distogram will be set to 1
        > it's a way to perform discretization of the distances, this model is used in AlphaFold3

        '''

        euclidean_distance=lambda coords1, coords2: float(np.sqrt(np.sum((coords1-coords2)**2)))
        L=X.shape[1] #number of residues

        if not isinstance(atoms,list):
            atoms=[atoms]
        k=len(atoms) #number of atoms used (distogram will be of dim L x L x k)

        if isinstance(Y, np.ndarray):
            raw_y=Y
        elif isinstance(Y, dict) and 'original' in list(Y.keys()):
            raw_y=Y['original']
        else:
            raise ValueError("Invalid input for Y: Expected numpy array or dictionary with 'original' key")
        
        Y_transformed = np.zeros((len(raw_y), L, L, k), dtype=float)
        max_distance = 0.0 #needed for discretization

        for s_idx in range(Y_transformed.shape[0]): #-- loop over all structures, create a distogram for each
            distogram=np.zeros((L,L,k),dtype=float)
            y_single_structure=raw_y[s_idx]
            for i in range(L):
                for j in range(L):
                    if i!=j:
                        for m,atom_idx in enumerate(atoms):
                            d=euclidean_distance(y_single_structure[i][atom_idx],y_single_structure[j][atom_idx])
                            distogram[i,j,m]=d
                            if d>max_distance:
                                max_distance=d
                    else:
                        for m,atom in enumerate(atoms):
                            distogram[i,j,m]=0.0                        

            Y_transformed[s_idx]=distogram #-- add distogram to the list of distograms

        # -- BUCKETING option
        if b and isinstance(b, int):
            new_Y_transformed=np.zeros((Y_transformed.shape[0], Y_transformed.shape[1], Y_transformed.shape[2], Y_transformed.shape[3], b), dtype=int)
            bucket_distance=max_distance/b
            for s_idx in range(Y_transformed.shape[0]):
                distogram=Y_transformed[s_idx]
                for i in range(L):
                    for j in range(L):
                        if i!=j: #if same residue no bucket should be filled
                            for m in range(k):
                                current_distance=distogram[i,j,m]
                                
                                bucket_idx=int(current_distance/bucket_distance)

                                if current_distance==max_distance: #if max distance, division wil yield an index out of bound (=b)
                                    bucket_idx=b-1

                                new_Y_transformed[s_idx,i,j,m,bucket_idx]=1
            Y_transformed=new_Y_transformed


        #--checking atoms dimension (3rd one), if only one atom is given squeeze it
        if Y_transformed.shape[3]==1:
            Y_transformed=np.squeeze(Y_transformed, axis=3)

        if isinstance(Y, dict):
            Y['Distogram'] = Y_transformed
        else:
            Y={'Original': Y, 'Distogram': Y_transformed}

        return super().transform(X, Y) 
        
def test():
    from IO.RNA_IO import RNA_IO
    from utils import pathify_pdb
    from viz import view_distogram

    rna_io=RNA_IO()
    pdb_path=pathify_pdb("7eaf")
    X,y= rna_io.read(pdb_path, "PDB")

    X,y=Distogram().transform(X,y,1,5)

    view_distogram(y)

if __name__=='__main__':
    test()