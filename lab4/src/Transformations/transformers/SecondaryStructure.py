import os,sys
sys.path.append(os.path.abspath('lab4/src'))

import numpy as np
class SecondaryStructure:
    
    def transform(self, X, Y):
        """
        Adds to Y the secondary structure of the sequences using the Nussinov algorithm with watson-crick distance constraints.
        The secondary structure is represented in dot-bracket notation.
        Parameters:
        - X: Input data (sequences array) of shape (num of sequences, num of residues).
        - Y: 3D coordinates array of atoms of shape (num of sequences, num of residues, max num of atoms, 3).
        Returns:
        - X: Input data (unchanged).
        - Y: Dictionary containing the original coordinates and the secondary structure.
        """
        
        if isinstance(Y, np.ndarray):
            Y = {"Original": Y}
        
        #Compute the center of mass for each residue in each sequence
        CoM_array=self._CoM(Y["Original"])
        
        #Compute the distance matrix for each sequence
        distograms=self._distograms(CoM_array)
        
        #Compute the secondary structure using Nussinov-WC algorithm
        structures=self._nussinov_wc_dist_batch(X, distograms)
        
        #Add the structures to the dictionary
        Y["SecondaryStructure"] = structures
        
        #Return the transformed data
        return X, Y


    def _CoM(self, Y):
        """
        Compute the center of mass for each residue, handling NaNs for both residues and atoms.

        Parameters:
        - Y: (num_sequences, max_residues, max_atoms, 3) NumPy array of atomic coordinates.

        Returns:
        - CoM_array: (num_sequences, max_residues, 3) NumPy array of center of mass coordinates.
        """
        #Initialize output array with NaNs 
        CoM_array = np.full((Y.shape[0], Y.shape[1], 3), np.nan)

        #Iterate through each sequence
        for i in range(Y.shape[0]):
            #Iterate through each residue
            for j in range(Y.shape[1]):
                #Extract atomic coordinates for this residue
                residue_atoms= Y[i, j]

                #Check if the residue is NaN (to handle padded sequences)
                if not np.isnan(residue_atoms).all():

                    #Compute the center of mass, ignoring NaNs
                    CoM_array[i, j] = np.nanmean(residue_atoms, axis=0)

        return CoM_array
    
    

    def _distograms(self, CoM_array):
        """
        Compute the distance matrix for each residue in a sequence, handling NaNs.
        Parameters:
        - CoM_array: (num_sequences, max_residues, 3) NumPy array of center of mass coordinates.
        Returns:
        - distograms: (num_sequences, max_residues, max_residues) NumPy array of distances.
        """
        #Initialize output array with NaNs
        distograms = np.full((CoM_array.shape[0], CoM_array.shape[1], CoM_array.shape[1]), np.nan)

        #Iterate through each sequence
        for i in range(CoM_array.shape[0]):
            #Iterate through each residue
            for j in range(CoM_array.shape[1]):
                #Extract center of mass coordinates for this residue
                residue_CoM = CoM_array[i, j]

                #Check if the residue is NaN (to handle padded sequences)
                if not np.isnan(residue_CoM).all():
                    #Compute the distances to all other residues
                    distances = np.linalg.norm(residue_CoM - CoM_array[i], axis=1)

                    #Store the distances in the distograms
                    distograms[i, j] = distances

        return distograms

    

    def _nussinov_wc_dist_batch(self, sequences, distance_matrices):
        """
        Batch processing of sequences and distance matrices for Nussinov algorithm with Watson-Crick distance constraints.
        Parameters:
        - sequences: 2D NumPy array of sequences (num_sequences, seq_length).
        - distance_matrices: 3D NumPy array of distance matrices (num_sequences, seq_length, seq_length).
        Returns:
        - structures: 2D NumPy array of structures in dot-bracket notation (num_sequences, seq_length).
        """
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
            
            #Call the modified Nussinov algorithm
            dot_bracket = self._nussinov_wc_dist(filtered_seq, filtered_dist_matrix)

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

    
    def _nussinov_wc_dist(self, seq, distograms):
        """
        Nussinov algorithm for RNA secondary structure prediction with distance constraints.
        Parameters:
        - seq: List of nucleotides (e.g., ["A", "U", "G", "C"]).
        - distograms: 2D NumPy array of distances between residues.
        Returns:
        - structure: List of dot-bracket notation for the secondary structure.
        """
        n = len(seq)
        M = np.zeros((n, n), dtype=int)  # DP table

        wc_pairs = {('A', 'U'), ('U', 'A'), ('G', 'C'), ('C', 'G')}
        
        for gap in range(1, n):
            for i in range(n - gap):
                j = i + gap
                
                best_score = M[i+1, j]  # Case: i is unpaired
                best_score = max(best_score, M[i, j-1])  # Case: j is unpaired
                
                if (seq[i], seq[j]) in wc_pairs and (2.7 <= distograms[i, j] <= 3.2):
                    best_score = max(best_score, M[i+1, j-1] + 1)

                for k in range(i, j):
                    best_score = max(best_score, M[i, k] + M[k+1, j])

                M[i, j] = best_score

        structure = ['.'] * n
        self.__traceback(M, seq, 0, n-1, structure, distograms, wc_pairs)
        
        return structure



    def __traceback(self, M, seq, i, j, structure, distograms, wc_pairs):
        """
        Traceback function to construct the secondary structure.
        Parameters:
        - M: DP table.
        - seq: List of nucleotides.
        - i, j: Indices for the current subsequence.
        - structure: List to store the dot-bracket notation.
        - distograms: 2D NumPy array of distances between residues.
        - wc_pairs: Set of valid Watson-Crick pairs.
        """
        if i >= j:
            return
        
        if M[i, j] == M[i+1, j]:
            self.__traceback(M, seq, i+1, j, structure, distograms, wc_pairs)
        elif M[i, j] == M[i, j-1]:
            self.__traceback(M, seq, i, j-1, structure, distograms, wc_pairs)
        elif M[i, j] == M[i+1, j-1] + 1 and (seq[i], seq[j]) in wc_pairs and (2.7 <= distograms[i, j] <= 3.2):
            structure[i] = '('
            structure[j] = ')'
            self.__traceback(M, seq, i+1, j-1, structure, distograms, wc_pairs)
        else:
            for k in range(i, j):
                if M[i, j] == M[i, k] + M[k+1, j]:
                    self.__traceback(M, seq, i, k, structure, distograms, wc_pairs)
                    self.__traceback(M, seq, k+1, j, structure, distograms, wc_pairs)
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
    
    
    #Example usage of Nussinov-WC distance batch
    sequences = np.array([
    ["A", "G", "C", "U", "A", "", ""],  #First sequence (padded)
    ["G", "C", "A", "U", "G", "C", ""]  #Second sequence (padded)
    ])

    distances = np.array([
        [
            [0.0, 3.1, 6.0, 2.8, 5.0, np.nan, np.nan],
            [3.1, 0.0, 2.9, 5.5, 3.0, np.nan, np.nan],
            [6.0, 2.9, 0.0, 3.2, 4.8, np.nan, np.nan],
            [2.8, 5.5, 3.2, 0.0, 3.1, np.nan, np.nan],
            [5.0, 3.0, 4.8, 3.1, 0.0, np.nan, np.nan],
            [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        ],
        [
            [0.0, 2.9, 5.0, 3.0, 2.7, 3.1, np.nan],
            [2.9, 0.0, 3.2, 5.5, 2.8, 3.0, np.nan],
            [5.0, 3.2, 0.0, 2.9, 4.1, 6.2, np.nan],
            [3.0, 5.5, 2.9, 0.0, 3.1, 5.0, np.nan],
            [2.7, 2.8, 4.1, 3.1, 0.0, 2.9, np.nan],
            [3.1, 3.0, 6.2, 5.0, 2.9, 0.0, np.nan],
            [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        ]
    ])

    structures = ss._nussinov_wc_dist_batch(sequences, distances)
    print(structures)
    for seq, struct in zip(sequences, structures):
        print("Sequence: ", "".join(seq))
        print("Structure:", "".join(struct))
