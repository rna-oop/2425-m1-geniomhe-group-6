import os,sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.BaseTransformer import BaseTransformer

class Normalize(BaseTransformer):
    
    def __init__(self, crop=True):
        self.crop = crop
        
    def transform(self, X, Y):
        """
        Normalizes the sequences by cropping them to the minimum length of sequences in the dataset if crop is True,
        otherwise returns the original sequences that are already padded.
        
        Parameters:
        - X: Input data (numpy array of sequences of nucleotides, with padding as empty strings).
        - Y: Output data (numpy array of x, y, z coordinates with dimensions 
        (num of sequences, max num of residues, max num of atoms, 3)).
    
        Returns:
        - The transformed X and Y sequences (cropped to the minimum length) if crop is True.
        - Otherwise, the original padded X and Y sequences are returned.
        - By calling the transform method of the parent class, the return value is either passed to the next transformer 
        in the chain or returned directly if it's the last transformer. 
        """
        
        if self.crop:
            
            #Find the minimum length of sequences by counting the number of non-empty nucleotides in each
            min_length = min([len([nucleotide for nucleotide in sequence if nucleotide != ""]) for sequence in X])
            
            #Crop the sequences to the minimum length
            X_transformed = [sequence[:min_length] for sequence in X]
            Y_transformed = [sequence[:min_length] for sequence in Y]
            
            #Return the transformed sequences and coordinates
            return super().transform(X_transformed, Y_transformed) 
        
        else: #If crop is False, return the original padded sequences and coordinates
            return super().transform(X, Y)