import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.BaseTransformer import BaseTransformer
import numpy as np

class Kmers(BaseTransformer):

    def __init__(self, k):
        self._k=k
    
    def transform(self, X, Y=None):
        """
        Transform the input data into k-mers.
        
        Parameters:
        - X: Input data (sequences array).
        - Y: coordinates array (not used in this transformation).
        
        Returns:
        - Transformed data as k-mers.
        """
        
        #Check if k is greater than 0
        if self._k <= 0:
            raise ValueError("k must be greater than 0")
        
        #Generate k-mers in numpy array
        X_transformed = np.empty((len(X), len(X[0]) - self._k + 1), dtype=object)

        #Iterate through each sequence and generate k-mers
        for i, seq in enumerate(X):
            kmers = [''.join(seq[j:j+self._k]) for j in range(len(seq) - self._k + 1)]
            for _ in range(len(kmers)):
                if len(kmers[_]) != self._k:
                    kmers[_]= '' 

            X_transformed[i] = kmers


        
        return super().transform(X_transformed, Y)
    
        