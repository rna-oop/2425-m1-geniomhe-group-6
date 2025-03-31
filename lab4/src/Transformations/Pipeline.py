import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.Normalize import Normalize
class Pipeline:
    
    def __init__(self, transformers):
        self.transformers = transformers

    def transform(self, X, Y):
        for transformer in self.transformers:
            if isinstance(transformer, Normalize) and self.transformers[0] != transformer:
                raise ValueError("Normalize transformer must be the first in the pipeline.")
            X, Y = transformer.transform(X, Y)
        return X, Y
    
