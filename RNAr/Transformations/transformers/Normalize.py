import os,sys
# sys.path.append(os.path.abspath('lab4/src'))

from RNAr.Transformations.transformers.BaseTransformer import BaseTransformer

import numpy as np

class Normalize(BaseTransformer):
    
    def __init__(self, crop=True):
        self.crop = crop
        
    def transform(self, X, Y):
        """
        Normalizes the sequences by cropping them to the minimum length of sequences in the dataset if crop is True,
        otherwise returns the original sequences that are already padded.
        
        :Parameters:
        - X: Input data (numpy array of sequences of nucleotides, with padding as empty strings).
        - Y: Output data (numpy array of x, y, z coordinates with dimensions 
        (num of sequences, max num of residues, max num of atoms, 3)).
    
        :Returns:
        - The transformed X and Y sequences (cropped to the minimum length) if crop is True.
        - Otherwise, the original padded X and Y sequences are returned.
        - By calling the transform method of the parent class, the return value is either passed to the next transformer 
        in the chain or returned directly if it's the last transformer. 
        """
        
        if self.crop:
            
            #Find the minimum length of sequences by ignoring only trailing empty strings at the end of each sequence
            min_length = min(len(sequence) - next((i for i, char in enumerate(reversed(sequence)) if char != ""), 0) for sequence in X)
            
            #Crop the sequences to the minimum length
            X_transformed = [sequence[:min_length] for sequence in X]
            Y_transformed = [sequence[:min_length] for sequence in Y]

            #Make the list a numpy array
            X_transformed = np.array(X_transformed)
            Y_transformed = np.array(Y_transformed)
            
            #Return the transformed sequences and coordinates
            return super().transform(X_transformed, Y_transformed) 
        
        else: #If crop is False, return the original padded sequences and coordinates
            return super().transform(X, Y)