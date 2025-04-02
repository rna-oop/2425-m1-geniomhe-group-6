'''
---------------------------------------------------------------------
    BaseTransformer.py
---------------------------------------------------------------------

BaseTransformer is an abstract class that serves as a base for all transformers in the pipeline.
It implements the interface Transformer than enforces the implementation of the transform and set_next methods,
the default behavior for chaining transformers and provides a method to display the transformer in a graph format (using graphviz, for __repr__ method).

set_next is implemented to make it inheritable directly to all ConcreteTransformers.  
The transform method is abstract and must be implemented by all subclasses.

'''
import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from abc import abstractmethod
from Transformations.transformers.Transformer import Transformer


from graphviz import Digraph

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

    def __display(self):
        """
        Recursive private method: Displays the transformer in form of a node, to be used in 
        
        initially transformations are chained as a linked list,
        and then the graph is built recursively from the last node to the header.
        """
        transformer_name = self.__class__.__name__
        params=''
        if len(self.__dict__)>1: #has attributes
            params = ', '.join([f"{k}={v}" for k, v in self.__dict__.items() if k != '_next_transformer'])

        if self._next_transformer:
            dot=self._next_transformer._display()
            current_node = dot.node(transformer_name, f"{transformer_name}\n{params}",shape="box", style="filled", fillcolor="lightblue")
            next_node_name = self._next_transformer.__class__.__name__
            dot.edge(transformer_name, next_node_name)
        else:
            dot = Digraph(format='fig')
            dot.node(transformer_name, f"{transformer_name}\n{params}",shape="box", style="filled", fillcolor="lightblue")

        return dot


    @abstractmethod
    def transform(self, X, Y):
        if self._next_transformer:
            return self._next_transformer.transform(X, Y)

        return X, Y