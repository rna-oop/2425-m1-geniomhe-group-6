import os,sys
sys.path.append(os.path.abspath('lab4/src'))

class Pipeline:
    
    def __init__(self, transformers):
        self.transformers = self._order(transformers)

    def transform(self, X, Y):
        for transformer in self.transformers:
            X, Y = transformer.transform(X, Y)
        return X, Y
    
    def _order(self, transformers):
        pass