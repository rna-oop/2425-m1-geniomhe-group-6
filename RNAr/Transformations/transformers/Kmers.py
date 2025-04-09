import os,sys
# sys.path.append(os.path.abspath('lab4/src'))

from RNAr.Transformations.transformers.BaseTransformer import BaseTransformer
from RNAr.Transformations.transformers.SecondaryStructure import SecondaryStructure
from RNAr.Transformations.transformers.TertiaryMotifs import TertiaryMotifs
import numpy as np

class Kmers(BaseTransformer):

    def __init__(self, k):
        self.k=k

    def set_next(self, transformer):
        if isinstance(transformer, SecondaryStructure) or isinstance(transformer, TertiaryMotifs):
            raise ValueError(f"OneHotEncoding transformer cannot be followed by {type(transformer)} transformer.")
        return super().set_next(transformer)
    
    def transform(self, X, Y=None):
        """
        Transform the input data into k-mers.
        
        :Parameters:
        - X: Input data (sequences array).
        - Y: coordinates array (not used in this transformation).
        
        :Returns:
        - Transformed data as k-mers.
        """
        
        #Check if k is greater than 0
        if self.k <= 0:
            raise ValueError("k must be greater than 0")
        
        #Generate k-mers in numpy array
        X_transformed = np.empty((len(X), len(X[0]) - self.k + 1), dtype=object)

        #Iterate through each sequence and generate k-mers
        for i, seq in enumerate(X):
            kmers = [''.join(seq[j:j+self.k]) for j in range(len(seq) - self.k + 1)]
            for _ in range(len(kmers)):
                if len(kmers[_]) != self.k:
                    kmers[_]= '' 

            X_transformed[i] = kmers


        
        return super().transform(X_transformed, Y)
    
        