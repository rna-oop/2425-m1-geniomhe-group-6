import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.BaseTransformer import BaseTransformer

class OneHotEncoding(BaseTransformer):
    
    def __init__(self):
        pass
        
    def transform(self, X, Y=None):
        
        
        return super().transform(X_transformed, Y) 