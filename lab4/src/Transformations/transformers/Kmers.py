import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.BaseTransformer import BaseTransformer

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
        
        #Generate k-mers
        X_transformed = []
        for seq in X:
            kmers = [seq[i:i+self._k] for i in range(len(seq) - self._k + 1)]
            X_transformed.append(kmers)
        
        return super().transform(X_transformed, Y)
    
        