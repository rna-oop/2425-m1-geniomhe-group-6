import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from abc import abstractmethod
from Transformations.transformers.Transformer import Transformer

class BaseTransformer(Transformer):
    """
    A base class for all transformers that implements the default behavior for chaining transformers.

    :Attributes:
    - _next_transformer: Holds the next transformer in the chain.

    :Methods:
    - set_next: Sets the next transformer in the chain and returns it.
    - transform: Performs the transformation and passes the data to the next transformer in the chain.
    """

    _next_transformer: Transformer = None

    def set_next(self, transformer: Transformer) -> Transformer:
        self._next_transformer = transformer
        return transformer

    @abstractmethod
    def transform(self, X, Y):
        if self._next_transformer:
            return self._next_transformer.transform(X, Y)

        return X, Y