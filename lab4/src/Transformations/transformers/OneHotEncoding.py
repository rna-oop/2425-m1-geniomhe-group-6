import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.BaseTransformer import BaseTransformer
from Transformations.transformers.Kmers import Kmers
class OneHotEncoding(BaseTransformer):
    
    def __init__(self):
        pass
    
    def set_next(self, transformer):
        if isinstance(transformer, Kmers):
            raise ValueError("OneHotEncoding transformer cannot be followed by Kmers transformer.")
        return super().set_next(transformer)
        
    def transform(self, X, Y=None):
        
        
        return super().transform(X_transformed, Y) 