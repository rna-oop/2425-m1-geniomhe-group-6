import os, sys
sys.path.append(os.path.abspath('lab4/src'))

from Transformations.transformers.BaseTransformer import BaseTransformer
from Transformations.transformers.SecondaryStructure import SecondaryStructure

from collections import defaultdict
import numpy as np

class TertiaryMotifs(BaseTransformer):
    
    
    def set_next(self, next_transformer):
        """
        Overrides the set_next method to ensure that the next transformer is not a SecondaryStructure instance.
        """
        if isinstance(next_transformer, SecondaryStructure):
            raise ValueError("SecondaryStructure transformer must be set before TertiaryMotifs")
        super().set_next(next_transformer)
        

    def transform(self, X, Y):
        """
        Checks if Y is a dictionary containing the key 'SecondaryStructure' and processes dot-bracket 
        notations for tertiary motif identification.

        Parameters:
        - X: Input data (not used in this implementation).
        - Y: Dictionary containing 'SecondaryStructure' key with dot-bracket format.

        Returns:
        - Y: Dictionary with 'TertiaryMotifs' key containing detected motifs for each sequence.
        """
        
        if not isinstance(Y, dict) or 'SecondaryStructure' not in Y:
            raise ValueError("Y must be a dictionary containing 'SecondaryStructure' key")
        
        dot_bracket_array = Y['SecondaryStructure']
        
        if not isinstance(dot_bracket_array, np.ndarray):
            raise ValueError("'SecondaryStructure' should be a numpy array")

        #Create a dictionary to store motifs for each sequence
        motifs_per_sequence = defaultdict(lambda: {
            "hairpins": [],
            "internal_loops": [],
            "bulges": [],
        })

        num_sequences, num_residues = dot_bracket_array.shape
        
        #Iterate over each sequence in the dot-bracket array
        for seq_idx in range(num_sequences):
            dot_bracket = dot_bracket_array[seq_idx]
            
            #Ensure each sequence is treated as a string
            dot_bracket = ''.join(dot_bracket)  
            
            #Detect motifs for this sequence
            self._detect_motifs(dot_bracket, motifs_per_sequence[seq_idx])
        
        #Add the motifs for each sequence to the Y dictionary
        Y['TertiaryMotifs'] = motifs_per_sequence

        #Return the transformed data
        return super().transform(X, Y)
    
    
    
    def _detect_motifs(self, dot_bracket, motifs):
        """
        Detects hairpins, internal loops, and bulges within a dot-bracket notation.

        Parameters:
        - dot_bracket: String representing the dot-bracket notation of an RNA sequence.
        - motifs: Dictionary where detected motifs will be stored.
        """
        #Detect hairpins
        self._detect_hairpins(dot_bracket, motifs)
        
        #Detect internal and bulge loops
        self._detect_loops(dot_bracket, motifs)
        

    
    
    def _detect_hairpins(self, dot_bracket, motifs, loop_size_threshold=3):
        """
        Detects hairpin motifs within a dot-bracket notation.
        Parameters:
        - dot_bracket: String representing the dot-bracket notation of an RNA sequence.
        - motifs: Dictionary where detected motifs will be stored.
        - loop_size_threshold: Minimum size of the loop to be considered a valid hairpin.
        """
        stack = []  #Stack to hold the positions of opening parentheses
        for i, char in enumerate(dot_bracket):
            if char == '(':  #Opening parenthesis -> start of a base-pair
                stack.append(i)
            elif char == ')':  #Closing parenthesis -> end of a base-pair
                start_idx = stack.pop()  #Get the matching opening index
                content= dot_bracket[start_idx + 1:i]  #Content between the parentheses
                loop_length = i - start_idx - 1  #Length of the loop (region between the parentheses)
                valid_hairpin = "."*loop_length  #Valid hairpin motif (all dots)
                if content == valid_hairpin and loop_length >= loop_size_threshold:  #Threshold for loop size 
                    #Store the hairpin motif (start and end indices of the stem, and loop length)
                    motifs["hairpins"].append({
                        "start": start_idx, 
                        "end": i, 
                    })
                    
                    
                    
    def _detect_loops(self, dot_bracket, motifs):
        """
        Detects internal loops and bulges within a dot-bracket notation.
        Parameters:
        - dot_bracket: String representing the dot-bracket notation of an RNA sequence.
        - motifs: Dictionary where detected motifs will be stored.
        """
        stack = []  #Stack to track the positions of opening parentheses
        prev_opened = -1  #To track the last opened parenthesis
        prev_closed = -1  #To track the last closed parenthesis
        current_opened = -1  #To track the current opened parenthesis
        current_closed = -1  #To track the current closed parenthesis
        for i, char in enumerate(dot_bracket):
            if char == '(':  #Opening parenthesis -> start of a base-pair
                stack.append(i)
                prev_opened = i  #Update the last opened parenthesis
            elif char == ')':  #Closing parenthesis -> end of a base-pair
                current_closed = i 
                if prev_closed != -1:
                    prev_opened = stack.pop()  #remove the last opened parenthesis
                    current_opened = stack[-1] #Get the matching opening index
                    if current_closed  - prev_closed > 1 and prev_opened - current_opened > 1:
                        #Store Internal loop motif (pair1 and pair2)
                        motifs["internal_loops"].append({
                            "pair1": (current_opened, current_closed),
                            "pair2": (prev_opened, prev_closed)
                        })
                    elif current_closed - prev_closed > 1:
                        #Store Bulge motif
                        motifs["bulges"].append({
                            "pair1": (current_opened, current_closed),
                            "pair2": (prev_opened, prev_closed)
                        })
                    elif prev_opened - current_opened > 1:
                        #Store Bulge motif
                        motifs["bulges"].append({
                            "pair1": (prev_opened, prev_closed),
                            "pair2": (current_opened, current_closed)
                        })
                    prev_closed = current_closed
                else:
                    prev_closed = i 




#Example usage:

if __name__ == "__main__":
    
    seq1= ['A', 'C', 'G', 'A', 'A', 'A', 'C', 'G', 'U']
    dot1=['(', '(', '(', '.','.','.',')', ')', ')','','','','',''] #Hairpin
    seq2= ['A', 'C', 'G', 'A', 'A', 'A', 'C', 'G', 'U', 'C', 'C', 'C', 'G', 'U']
    dot2=['(', '(', '(', '.', '.', '(', '(', ')', ')', '.', '.', ')', ')', ')'] #Internal loop
    seq3= ['A', 'C', 'G', 'A', 'C', 'G', 'U', 'C', 'C', 'C', 'G', 'U']
    dot3=['(', '(', '(', '(', '(',  ')', ')', '.', '.', ')', ')', ')','',''] #Bulge

    tm= TertiaryMotifs()

    dict1={"hairpins": []}
    tm._detect_hairpins("".join(dot1), dict1)
    print(dict1)

    dict2={"internal_loops": []}
    tm._detect_loops(dot2, dict2)
    print(dict2)

    dict3={"bulges": []}
    tm._detect_loops(dot3, dict3)
    print(dict3)

    #Example usage for transform method
    X = None 
    Y = {
        'SecondaryStructure': np.array([dot1, dot2, dot3])
    }
    X,Y=tm.transform(X, Y)
    print(Y)
