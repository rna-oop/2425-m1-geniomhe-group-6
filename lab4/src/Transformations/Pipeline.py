'''
------------------------------------------------------------------------------------
                                pipeline module
------------------------------------------------------------------------------------

Home for Pipeline class

classes in this module are used to create a pipeline of transformations to be applied
RNA structure data (as numpy arrays) to be used in ML models.

this will be built by taking into consideration  
- pipeline module interface from scikit-learn
- transformations being implemented using the CoR design pattern

------------------------------------------------------------------------------------
'''

import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.Transformer import Transformer
from Transformations.transformers.Normalize import Normalize
class Pipeline:
    
    def __init__(self, transformers):
        
        #Ensure the transformers are valid classes and that the first one is Normalize if present
        for i, transformer in enumerate(transformers):
            if not isinstance(transformer, Transformer):
                raise ValueError(f"{transformer} is invalid transformer.")
            if isinstance(transformer, Normalize) and i != 0:
                raise ValueError("Normalize transformer must be the first in the pipeline.")
            
        self.transformers = transformers
        
        #Set the next transformer in the chain for each transformer
        for i in range(len(self.transformers)-1):
            self.transformers[i].set_next(self.transformers[i+1])


    def transform(self, X, Y):
        
        if not self.transformers:
            return X, Y  #No transformation if pipeline is empty
        
        #Start transformation from the first transformer
        return self.transformers[0].transform(X, Y)
    
