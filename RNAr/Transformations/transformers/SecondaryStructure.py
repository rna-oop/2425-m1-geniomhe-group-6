import os,sys
# sys.path.append(os.path.abspath('lab4/src'))

from RNAr.Transformations.transformers.BaseTransformer import BaseTransformer

import numpy as np
class SecondaryStructure(BaseTransformer):
    
    def __init__(self, nussinov=False):
        self.nussinov = nussinov


    def transform(self, X, Y):
        """
        Adds to Y the secondary structure of the RNA sequences in X using either the Nussinov algorithm or Watson-Crick distance constraints.
        The secondary structure is represented in dot-bracket notation.
        
        :Parameters:
        - X: Input data (sequences array) of shape (num of sequences, num of residues).
        - Y: 3D coordinates array of atoms of shape (num of sequences, num of residues, max num of atoms, 3).

        :Returns:
        - X: Input data (unchanged).
        - Y: Dictionary containing the original coordinates and the secondary structure.
        """
        
        if isinstance(Y, np.ndarray):
            Y = {"Original": Y}
        
        if self.nussinov:
            #Compute the secondary structure using Nussinov algorithm
            structures=self._nussinov_batch(X)
        
        else:
            #Compute the center of mass for each residue in each sequence
            CoM_array=self._CoM(Y["Original"])
        
            #Compute the distance matrix for each sequence
            distograms=self._distograms(CoM_array)
        
            #Compute the secondary structure using Watson-Crick distance constraints
            structures = self._WDistances_batch(X, distograms)
        
        #Add the structures to the dictionary
        Y["SecondaryStructure"] = structures
        
        #Return the transformed data
        return super().transform(X, Y)  #Call the parent class's transform method to continue the transformation chain





    def _CoM(self, Y):
        """
        Compute the center of mass for each residue, handling NaNs.

        :Parameters:
        - Y: (num_sequences, max_residues, max_atoms, 3) NumPy array of atomic coordinates.

        :Returns:
        - CoM_array: (num_sequences, max_residues, 3) NumPy array of center of mass coordinates.
        """
        #Compute mean along axis=2 (atoms), ignoring NaNs
        CoM_array = np.nanmean(Y, axis=2)
        return CoM_array
    





    def _distograms(self, CoM_array):
        """
        Compute Euclidean distance matrices for each sequence, handling NaNs. 

        :Parameters:
        - CoM_array: (num_sequences, num_residues, 3) NumPy array of center of mass coordinates.

        :Returns:
        - distograms: (num_sequences, num_residues, num_residues) NumPy array of distances, with NaNs where necessary.
        """

        #Compute pairwise differences using broadcasting
        diffs = CoM_array[:, :, np.newaxis, :] - CoM_array[:, np.newaxis, :, :]  #Shape: (num_sequences, num_residues, num_residues, 3)

        #Compute Euclidean distances (L2 norm) along the last axis (x, y, z)
        distograms = np.linalg.norm(diffs, axis=-1)  #Shape: (num_sequences, num_residues, num_residues)

        #Mask invalid distances where either residue is NaN
        invalid_mask = np.isnan(CoM_array).any(axis=-1)  #Shape: (num_sequences, num_residues)
        distograms[np.broadcast_to(invalid_mask[:, :, np.newaxis], distograms.shape) |
                np.broadcast_to(invalid_mask[:, np.newaxis, :], distograms.shape)] = np.nan

        return distograms

    
    
    
    def _WDistances_batch(self, sequences, distance_matrices):
        
        num_sequences, seq_length = sequences.shape
        structures = np.full((num_sequences, seq_length), "", dtype=object)  #Initialize with empty strings
        
        for seq_idx in range(num_sequences):
            seq = sequences[seq_idx]
            dist_matrix = distance_matrices[seq_idx]

            #Get valid residues (ignore empty residues)
            valid_mask = np.array([res != "" for res in seq])
            valid_indices = np.where(valid_mask)[0]
            
            #Filter sequence and distance matrix
            filtered_seq = [seq[i] for i in valid_indices]
            filtered_dist_matrix = dist_matrix[np.ix_(valid_indices, valid_indices)]
            
            #Call the Watson-Crick distance function
            dot_bracket = self.__WDistances(filtered_seq, filtered_dist_matrix)

            #Reintroduce padding: map back to original indices
            for i, idx in enumerate(valid_indices):
                structures[seq_idx, idx] = dot_bracket[i]

            #Ensure non-paired residues remain "." but empty ones stay ""
            for j in range(seq_length):
                if structures[seq_idx, j] == "":  #Keep empty residues as ""
                    continue
                if structures[seq_idx, j] not in {"(", ")"}:  #Non-paired residues get "."
                    structures[seq_idx, j] = "."

        return structures
    
    
    
    
    def __WDistances(self, seq, distogram):
        """
        Watson-Crick distance constraints for secondary structure prediction.

        :Parameters:
        - seq: List of nucleotides (e.g., ["A", "U", "G", "C"]).
        - distogram: 2D NumPy array of distances between residues.

        :Returns:
        - structure: List of dot-bracket notation for the secondary structure.
        """
        #Initialize the structure with dots
        structure = ['.'] * len(seq)
        
        #Valid Watson-Crick pairs
        valid_pairs = {("A", "U"), ("U", "A"), ("G", "C"), ("C", "G")}
        
        #Iterate through the sequence and distance matrix
        #Check for valid pairs and distance constraints
        for i in range(len(seq)):
            for j in range(i + 1, len(seq)):
                if (seq[i], seq[j]) in valid_pairs and (8.6 <= distogram[i, j] <= 10.8):
                    structure[i] = "("
                    structure[j] = ")"
                    break
        
        return structure
    
    
    
    
    
    def _nussinov_batch(self, sequences):
        """
        Batch processing of sequences for Nussinov algorithm.

        :Parameters:
        - sequences: 2D NumPy array of sequences (num_sequences, seq_length).

        :Returns:
        - structures: 2D NumPy array of structures in dot-bracket notation (num_sequences, seq_length).
        """
        num_sequences, seq_length = sequences.shape
        structures = np.full((num_sequences, seq_length), "", dtype=object)  #Initialize with empty strings

        for seq_idx in range(num_sequences):
            seq = sequences[seq_idx]

            #Get valid residues (ignore empty residues)
            valid_mask = np.array([res != "" for res in seq])
            valid_indices = np.where(valid_mask)[0]
            
            #Filter sequence 
            filtered_seq = [seq[i] for i in valid_indices]
            
            #Call the Nussinov algorithm
            dot_bracket = self.__nussinov(filtered_seq)

            #Reintroduce padding: map back to original indices
            for i, idx in enumerate(valid_indices):
                structures[seq_idx, idx] = dot_bracket[i]

            #Ensure non-paired residues remain "." but empty ones stay ""
            for j in range(seq_length):
                if structures[seq_idx, j] == "":  #Keep empty residues as ""
                    continue
                if structures[seq_idx, j] not in {"(", ")"}:  #Non-paired residues get "."
                    structures[seq_idx, j] = "."

        return structures

    
    
    
    def __nussinov(self, seq):
        """
        Nussinov algorithm for RNA secondary structure prediction.
        :Parameters:
        - seq: List of nucleotides (e.g., ["A", "U", "G", "C"]).
        :Returns:
        - structure: List of dot-bracket notation for the secondary structure.
        """
        n = len(seq)
        M = np.zeros((n, n), dtype=int)  #DP table

        wc_pairs = {('A', 'U'), ('U', 'A'), ('G', 'C'), ('C', 'G')}
        
        for gap in range(1, n):
            for i in range(n - gap):
                j = i + gap
                
                best_score = M[i+1, j]  #Case: i is unpaired
                best_score = max(best_score, M[i, j-1])  #Case: j is unpaired
                
                if (seq[i], seq[j]) in wc_pairs:
                    best_score = max(best_score, M[i+1, j-1] + 1)

                for k in range(i, j):
                    best_score = max(best_score, M[i, k] + M[k+1, j])

                M[i, j] = best_score

        structure = ['.'] * n
        self.__traceback(M, seq, 0, n-1, structure, wc_pairs)
        
        return structure



    def __traceback(self, M, seq, i, j, structure, wc_pairs):
        """
        Traceback function to construct the secondary structure.
        :Parameters:
        - M: DP table.
        - seq: List of nucleotides.
        - i, j: Indices for the current subsequence.
        - structure: List to store the dot-bracket notation.
        - wc_pairs: Set of valid Watson-Crick pairs.
        """
        if i >= j:
            return
        
        if M[i, j] == M[i+1, j]:
            self.__traceback(M, seq, i+1, j, structure, wc_pairs)
        elif M[i, j] == M[i, j-1]:
            self.__traceback(M, seq, i, j-1, structure, wc_pairs)
        elif M[i, j] == M[i+1, j-1] + 1 and (seq[i], seq[j]) in wc_pairs:
            structure[i] = '('
            structure[j] = ')'
            self.__traceback(M, seq, i+1, j-1, structure, wc_pairs)
        else:
            for k in range(i, j):
                if M[i, j] == M[i, k] + M[k+1, j]:
                    self.__traceback(M, seq, i, k, structure, wc_pairs)
                    self.__traceback(M, seq, k+1, j, structure, wc_pairs)
                    break





if __name__ == "__main__":
    # Example usage
    Y = np.array([[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]])
    print("Input Array:")
    print(Y)
    print(Y.shape)
    
    ss = SecondaryStructure()
    
    CoM_array = ss._CoM(Y)
    print("Center of Mass Array:")
    print(CoM_array)
    print(CoM_array.shape)
    
    distograms = ss._distograms(CoM_array)
    print("Distance Matrix:")
    print(distograms)
    print(distograms.shape)
    
    
    #Example with more sequences and Nans values
    Y = np.array([[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
                  [[[13, 14, 15], [16, 17, 18]], [[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]]]])
    print("Input Array:")
    print(Y)
    print(Y.shape)
    CoM_array = ss._CoM(Y)
    print("Center of Mass Array:")
    print(CoM_array)
    print(CoM_array.shape)
    distograms = ss._distograms(CoM_array)
    print("Distance Matrix:")
    print(distograms)
    print(distograms.shape)
    
    #Example with Watson-Crick distance constraints
    from utils import parse_pdb_files
    X,Y=parse_pdb_files(["7eaf"])
    print(X.shape)
    print(Y.shape)
    X_transformed,Y_transformed=ss.transform(X,Y)
    print("".join(Y_transformed["SecondaryStructure"][0]))
    
    #Example with Nussinov algorithm
    ss1 = SecondaryStructure(nussinov=True)
    X_transformed,Y_transformed=ss1.transform(X,Y)
    print("".join(Y_transformed["SecondaryStructure"][0]))
    