from itertools import product
import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.BaseTransformer import BaseTransformer
from Transformations.transformers.Kmers import Kmers

import numpy as np


class OneHotEncoding(BaseTransformer):
    ALPHABET=['A','C','U','G'] #-- class attribute (defining ordered RNA alphabet, other excpetional and unusual residues can be considered in future model by just simply adding them to this list)
    
    def __init__(self):
        pass
    
    def set_next(self, transformer):
        if isinstance(transformer, Kmers):
            raise ValueError("OneHotEncoding transformer cannot be followed by Kmers transformer.")
        return super().set_next(transformer)
        
    def transform(self, X, Y=None):
        '''
        `OneHotEncoding().transform(X)`: transforms a numpy array representing RNA kmers (or base pairs, i.e. kmers of length 1)
        into a nd array of all possible kmers on the columns and the ones in X on the rows: 
        values are binary (0 or 1) indicating the presence of a kmer in the sequence.  

        :Parameters:
        - X: Input data (numpy array of sequences of nucleotides/kmers)
            
        :Returns:
        - transformed_X: ndarray of 1s and 0s
        - Y: coordinates array (not used in this transformation) but returned for information saving purposes

        :Logic:
        this method will function always as if its taking a kmers numpy array as input, for the sake of consistency
        as it is possible to pipe it after Kmers transformer

        > p.s. it will be 3-dimensional: d1= for the number of sequences, d2= for the number of kmers in each sequence, d3= for the number of kmers combinations (4^k)  
        '''

        k=len(X[0]) if len(X.shape)==1 else len(X[0][0])
        colnames_all_kmers=["".join(i) for i in product(self.ALPHABET, repeat=k)] #--successful (ordered by A, C, U, G)
        
        X_transformed=np.zeros((X.shape[0],X.shape[1],len(colnames_all_kmers)),dtype=int)

        for i, seq in enumerate(X):
            for j, kmer in enumerate(seq):
                if j=='':
                    continue
                index=colnames_all_kmers.index(kmer)
                X_transformed[i,j,index]=1

        
        return super().transform(X_transformed, Y) 