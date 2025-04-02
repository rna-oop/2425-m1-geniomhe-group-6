'''
------------------------------------------------------------------------------------
                                pipeline module
------------------------------------------------------------------------------------

Home for Pipeline classe

classes in this module are used to create a pipleine of transformations to be applied
RNA structure data (as numpy arrays) to be used in ML models.

this will be built by taking into consideration  
- pipeline module interface from scikit-learn
- transformations being implemented using the CoR design pattern

------------------------------------------------------------------------------------
'''

import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.Normalize import Normalize
class Pipeline:
    
    def __init__(self, transformers):
        self.transformers = transformers
        for i in range(len(self.transformers)-1):
            self.transformers[i].set_next(self.transformers[i+1])

    def transform(self, X, Y):
        for transformer in self.transformers:
            if isinstance(transformer, Normalize) and self.transformers[0] != transformer:
                raise ValueError("Normalize transformer must be the first in the pipeline.")
            X, Y = transformer.transform(X, Y)
        return X, Y
    
