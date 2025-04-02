'''
visualization module: functions to visualize rna data representations

each transformation can provide a different rna representation, these functions cretae an interactive figure to portray each

- view_distogram: takes a dict of y transformations, and viz the distogram through interactive landscape and heatmaps
- view_one_hot: takes an one-hot-encoded X nd array and visualize inf the form of a table

'''

import plotly.graph_objects as go
import numpy as np
import math
from itertools import product
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import numpy as np

from draw_rna.ipynb_draw import draw_struct

colors4 = ['#B7094C', '#0E87A6','#02B693','#DEAD03' ]
color_maps = ['viridis', 'plasma', 'magma', 'cividis', 'inferno', 'YlGnBu', 'YlOrRd', 'Blues', 'Greens', 'Reds']


def generate_gradient(colors, n=4,plot=False):
    """Generate a gradient of colors from a list of colors."""
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors, N=n)
    
    values = np.linspace(0, 1, n)
    
    gradient_colors = [cmap(value) for value in values]

    if plot:
        plt.figure(figsize=(8, 2))
        plt.imshow(gradient_colors, aspect='auto')
        plt.axis('off')
        plt.title("Color Gradient")
        plt.show()
    
    return gradient_colors

def view_distogram(y_transformed: dict, 
                    structure_no=0, 
                    colormaps=None,
                    width=None,
                    height=None,
                    plot=True,
                    save=False,
                    path=None):
    '''
    takes a dict of y transformations, and viz the distogram through interactive landscape and heatmaps
    
    parameters:
    - y_transformed: dict of y transformations (works also on the distograms saved in ndarray)
    - structure_no: index of the structure to visualize (default is 0)
    - colormaps: list of colormaps to use for the distogram (default is a list of 10 colormaps foudn as global attribute in this module)
    - width: fig width (optional)
    - height: fig height (optional)
    - plot: boolean to show the figure (default is True)
    - save: boolean to save the figure as html (default is False)
    - path: str, file name/path, if save if False but path is provided it will still save in the specified path,
            else if path not provided but save is True saves to default filename 'distogram_<structure_no>_<shape>.html' in wd

    returns:
    - fig (plotly figure): interactive distogram visualization
    
    '''
    if isinstance(y_transformed, dict):
        y_transformed = y_transformed['Distogram']

    if colormaps is None:
        colormaps = color_maps

    fig = go.Figure()
    distogram = y_transformed[0]
    dims=str(distogram.shape).replace(', ','x')
    traces = []
    title_add=""
    
    match y_transformed.dtype:
        case 'int64':
            title_add+=' discretized'
            if distogram.ndim == 3:
                distogram = np.expand_dims(distogram, axis=2)
            num_atoms = distogram.shape[2]
            
            for idx in range(num_atoms):
                x = np.arange(distogram.shape[0])
                y = np.arange(distogram.shape[1])
                X, Y = np.meshgrid(x, y)
                Z = np.zeros_like(X)
                
                for i in range(distogram.shape[0]):
                    for j in range(distogram.shape[1]):
                        for k in range(distogram.shape[3]):
                            if distogram[i, j, idx, k] == 1:
                                Z[i, j] = k
                
                traces.append(go.Surface(
                    z=Z, x=X, y=Y, colorscale=colormaps[idx], opacity=0.5, name=f"atom {idx+1} in list layer", showscale=False
                ))
                
        
        case 'float64':
            num_atoms = 1 if distogram.ndim == 2 else distogram.shape[2]
            if num_atoms == 1:
                distogram = np.expand_dims(distogram, axis=2)
            
            for i in range(num_atoms):
                data = distogram[:, :, i]
                x = np.arange(data.shape[1])
                y = np.arange(data.shape[0])
                X, Y = np.meshgrid(x, y)
                
                traces.append(go.Surface(
                    z=data, x=X, y=Y, colorscale=colormaps[i], showscale=False, opacity=0.5, name=f"atom {i+1} in list layer"
                ))
    
    # Add traces to figure
    for trace in traces:
        fig.add_trace(trace)
    
    # Button to toggle which trace appears on top
    buttons = []
    for i in range(len(traces)):
        order = list(range(len(traces)))
        order.append(order.pop(i))  # Move selected trace to the last position
        
        buttons.append({
            "label": f"{traces[i].name} to Top",
            "method": "update",
            "args": [{"x": [traces[j].x for j in order], "y": [traces[j].y for j in order], "z": [traces[j].z for j in order]}]
        })
    
    fig.update_layout(
        title=f'3D vis distogram {dims} landscape{title_add}',
        scene=dict(xaxis_title="X-axis residues", yaxis_title="Y-axis residues", zaxis_title="Distance"),
        margin=dict(l=10, r=10, t=30, b=10),
        updatemenus=[{"buttons": buttons, "direction": "down", "showactive": True}]
    )

    if width:
        fig.update_layout(width=width)
    if height:
        fig.update_layout(height=height)
    
    if plot:
        fig.show()
    if save or path is not None:
        if path is not None:
            fig.write_html(path) #-- add validation of a path later on
        else:
            fig.write_html(f"distogram_{structure_no}_{dims}_{title_add}.html")
    
    return fig


def view_one_hot(X, 
                 structure_no=0,
                 width=None,
                 height=None,
                 y_ticks=False,
                 plot=True,
                 save=False, 
                 path=None):
    """
    Visualize the one-hot encoded matrix for a given structure

    first starts by reconstructing the colnames, the idea is the ncols=4^k (if encoded directly on seq will be k=1, if kmerized before will get the k)
    then will reconstruct the colnames for the one-hot encoding (all combinations of kmers of length k)
    and then will plot the one-hot encoding as a heatmap

    paramters:
    - X: one-hot encoded matrix
    - structure_no: index of the structure to visualize (default is 0)
    - width: width of the figure (defaulting to cell-based scaling)
    - height: height of the figure (defaulting to cell-based scaling)
    - plot: boolean to show the figure (default is True)
    - save: boolean to save the figure as html (default is False)
    - path: str of path where to save it, if save=F but path provided will still save, if path not provided will save in default filename in wd (default None)

    returns:
    - fig (plotly figure): heatmap of the one-hot encoded matrix

    """
    data=X[structure_no]

    alphabet=['A','C','U','G']
    k=int(math.log2(X.shape[2])/math.log2(4))
    all_kmers_comb_reconstructed =["".join(i) for i in product(alphabet, repeat=k)]
    
    col_names = all_kmers_comb_reconstructed
    row_names = [f"{i+1}" for i in range(data.shape[0])]

    custom_colors=generate_gradient(colors4, n=len(col_names), plot=False)
    custom_colorscale = []
    for col_idx, custom_color in enumerate(custom_colors[:len(col_names)]):
        custom_colorscale.append([col_idx / len(col_names), 'white'])  # Map 0 to white
        custom_colorscale.append([(col_idx + 0.5) / len(col_names), custom_color])  # Map 1 to the column's base color

    black_white=[0,'white'],[1,'black']

    fig = go.Figure(data=go.Heatmap(
        z=data,
        colorscale=black_white,  
        showscale=False
    ))

    cell_size = 70  # Adjust this value for larger/smaller squares

    if width is not None:
        fig_width = width
    else:
        fig_width = cell_size * len(col_names)

    if height is not None:
        fig_height = height
    else:
        fig_height = int(cell_size * len(row_names) * 0.45 )


    fig.update_layout(
        height=fig_height,
        width=fig_width,
        title="Binary Matrix Visualization",
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(col_names))),
            ticktext=col_names,
            tickside='top',
            tickangle=-45
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(len(row_names))) if y_ticks else [],
            ticktext=row_names
        ),
        plot_bgcolor='white'
    )
    if plot:
        fig.show()

    if save or path is not None:
        if path is not None:
            fig.write_html(path)
        else:
            fig.write_html(f"one_hot_{structure_no}_{k}mer.html")
        
    return fig

def view_ss_arcs(X, y, sequence_no:int=None):
    """
    Visualizes RNA sequences and their secondary structure with base pair arcs: built using matplotlib
    
    Parameters:
    - X (sequences): NumPy array of RNA sequences (shape: num_sequences, max_residues), padded with empty strings.
    - y (dot_brackets): NumPy array of lists containing dot-bracket strings (shape: num_sequences, max_residues) | or y in form of dict containing ss in y['SecondaryStructure']
    - sequence_no: int specifying the index of the sequence to visualize (default: None, visualizes all sequences).
    
    Returns:
    - Displays the RNA structure as a plot. 
    """

    sequences = X
    if isinstance(y, dict):
        dot_brackets = y['SecondaryStructure']
    else:
        dot_brackets = y


    num_sequences = sequences.shape[0]

    if sequence_no is not None:
        num_sequences=1
    
    # Ensure axes is iterable (for single sequence case)
    if num_sequences == 1:
        axes = [plt.gca()]
    else:
        fig, axes = plt.subplots(num_sequences, 1, figsize=(10, 2 * num_sequences))
    
    # Iterate through each sequence and its corresponding dot-bracket
    for idx in range(num_sequences):

        if sequence_no is not None: # --it will be one iteration of the loop and idx is reset
            idx=sequence_no

        seq = sequences[idx]
        dot_bracket = dot_brackets[idx]
        ax = axes[idx]
        
        ax.set_title(f"RNA Sequence {idx + 1}\n")

        # Remove padding (empty strings)
        valid_indices = np.where(seq != "")[0]
        valid_seq = [seq[i] for i in valid_indices]
        valid_dot_bracket = [dot_bracket[i] for i in valid_indices]

        # Convert dot-bracket to coordinates
        positions = np.arange(len(valid_seq))
        base_pairs = []

        # Find base pairs from dot-bracket using stack
        stack = []
        for i, char in enumerate(valid_dot_bracket):
            if char == '(':
                stack.append(i)
            elif char == ')':
                pair = stack.pop()
                base_pairs.append((pair, i))

        # Create a circular plot for the RNA sequence
        num_residues = len(valid_seq)
        angle_step = 2 * np.pi / num_residues
        angles = np.arange(0, 2 * np.pi, angle_step)

        # Plot the sequence as dots in a circle
        for i, angle in enumerate(angles):
            x = np.cos(angle)
            y = np.sin(angle)
            ax.plot(x, y, 'ko', markersize=1, color='darkblue')  # RNA residue positions
            ax.text(x * 1.1, y * 1.1, valid_seq[i], ha='center', va='center', fontsize=8, color='darkorchid')
        
        # Draw arcs for base pairs
        for start, end in base_pairs:
            start_angle = angles[start]
            end_angle = angles[end]
            ax.plot([np.cos(start_angle), np.cos(end_angle)], 
                    [np.sin(start_angle), np.sin(end_angle)], 
                    color='skyblue', lw=1)

        ax.set_aspect('equal', 'box')
        ax.axis('off')  # Turn off the axis for clarity
        
        # Handle padding and show the full dot-bracket structure
        full_structure = ['' if seq[i] == '' else '.' for i in range(len(seq))]
        for i, idx in enumerate(valid_indices):
            full_structure[idx] = valid_dot_bracket[i]
        
        # Print the full dot-bracket sequence, keeping empty residues as ''
        print(f"Full structure for Sequence {idx + 1}: {''.join(full_structure)}")

    plt.tight_layout()
    plt.show()

def view_ss_network(X, y, filename_prefix="rna_network", sequence_no:int=None):
    """
    Plots RNA sequences as network graphs based on dot-bracket notation: build on networkx and pyvis, saves interactive network as html in wd
    
    Parameters:
    - X (sequences): NumPy array of RNA sequences (shape: num_sequences, max_residues), padded with empty strings.
    - y (dot_brackets): NumPy array of lists containing dot-bracket strings (shape: num_sequences, max_residues) || disctionary containing the numpy array
    - filename_prefix: Prefix for output HTML files (default: "rna_network").
    - sequence_no: int specifying the index of teh sequence to visualize (set if dont wanna viz all sequences) (default: None)
    
    Displays network plots for RNA secondary structures.
    """

    sequences = X
    if isinstance(y, dict):
        dot_brackets = y['SecondaryStructure']
    else:
        dot_brackets = y

    num_sequences = sequences.shape[0]

    if sequence_no is not None:
        num_sequences=1
    
    for idx in range(num_sequences):

        if sequence_no is not None: # --it will be one iteration of the loop and idx is reset
            idx=sequence_no

        seq = sequences[idx]
        dot_bracket = dot_brackets[idx]
        
        # Remove padding
        valid_indices = np.where(seq != "")[0]
        valid_seq = [seq[i] for i in valid_indices]
        valid_dot_bracket = [dot_bracket[i] for i in valid_indices]
        
        G = nx.Graph()
        net = Network(height="800px", width="100%", notebook=True)
        stack = []
        base_pairs = []
        
        for i, char in enumerate(valid_dot_bracket):
            if char == "(":
                stack.append(i)
            elif char == ")":
                start = stack.pop()
                end = i
                base_pairs.append((start, end))
        
        for i in range(len(valid_dot_bracket)):
            G.add_node(i, label=valid_seq[i])
            net.add_node(i, label=valid_seq[i], size=10)
        
        for i in range(len(valid_dot_bracket) - 1):  # Link sequential bases
            G.add_edge(i, i + 1)
            net.add_edge(i, i + 1, color="gray")
        
        for pair in base_pairs:  # Link base pairs
            G.add_edge(pair[0], pair[1])
            net.add_edge(pair[0], pair[1], color="red")
        
        net.force_atlas_2based()
        net.show(f"{filename_prefix}_{idx+1}.html")
        
        plt.figure(figsize=(12, 8))
        pos = nx.circular_layout(G)  # Ensure circular layout
        labels = {i: valid_seq[i] for i in range(len(valid_seq))}
        
        # Draw edges with different colors
        nx.draw_networkx_edges(G, pos, edgelist=[(i, i + 1) for i in range(len(valid_dot_bracket) - 1)], edge_color="gray", width=1)
        nx.draw_networkx_edges(G, pos, edgelist=base_pairs, edge_color="darkmagenta", width=1)
        
        nx.draw_networkx_nodes(G, pos, node_size=140, node_color="skyblue")
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=7)
        
        plt.title(f"RNA Network Structure {idx + 1}")
        plt.axis("off")
        plt.show()

def view_ss_2d(X, y, sequence_no:int=None, *args,**kwargs):
    """
    Visualizes RNA sequences and their secondary structure representation using the draw_rna library
    
    Parameters:
    - X (sequences): NumPy array of RNA sequences (shape: num_sequences, max_residues), padded with empty strings.
    - y (dot_brackets): NumPy array of lists containing dot-bracket strings (shape: num_sequences, max_residues) || or y in form of dict containing ss in y['SecondaryStructure']
    - sequence_no: int specifying the index of the sequence to visualize (default: None, visualizes all sequences).
    
    *args and **kwargs are possible arguments to be given to the library's function (for options, help(draw_rna.ipynb_dra.draw_struct))
    
    Returns:
    - Displays the RNA structure as a plot. 
    """

    sequences = X
    if isinstance(y, dict):
        dot_brackets = y['SecondaryStructure']
    else:
        dot_brackets = y


    num_sequences = sequences.shape[0]

    if sequence_no is not None:
        num_sequences=1

    for idx in range(num_sequences):

        if sequence_no is not None: # --it will be one iteration of the loop and idx is reset
            idx=sequence_no

        seq = sequences[idx]
        seq=str(''.join(seq))

        struct= dot_brackets[idx]
        struct=str(''.join(struct))

        print(f'seq {len(seq)}: {seq}')
        print(f'struct {len(struct)}: {struct}')

        draw_struct(seq, struct)
    

############### deprecated ######################



# def old_view_distogram(y_transformed:dict, 
#                     structure_no=0, 
#                     colormaps=['viridis', 'plasma', 'magma', 'cividis', 'inferno', 'YlGnBu', 'YlOrRd', 'Blues', 'Greens', 'Reds'],
#                     plot=True,
#                     save=False):
#     '''
#     takes a dict of y transformations, and viz the distogram through interactive landscape and heatmaps
    
#     parameters:
#     - y_transformed: dict of y transformations (works also on the distograms saved in ndarray)
#     - structure_no: index of the structure to visualize (default is 0)
#     - colormaps: list of colormaps to use for the distogram (default is a list of 10 colormaps)
#     - plot: boolean to show the figure (default is True)
#     - save: boolean to save the figure as html (default is False)

#     returns:
#     - fig (plotly figure): interactive distogram visualization
    
#     '''
#     if isinstance(y_transformed,dict): #temp for testing
#         y_transformed=y_transformed['Distogram'] #

#     fig = go.Figure()
#     colormaps=['viridis', 'plasma', 'magma', 'cividis', 'inferno', 'YlGnBu', 'YlOrRd', 'Blues', 'Greens', 'Reds']
#     distogram=y_transformed[0]

#     match y_transformed.dtype:
#         case 'int64': #if bucketized => discrete landscape

#             if distogram.ndim==3:
#                 # -- expand 3rd dim to be 1 (limits errors)
#                 distogram=np.expand_dims(distogram, axis=2)

#             num_atoms=distogram.shape[2] #-- number of atoms in distogram

#             for idx in range(distogram.shape[2]):
#                 x = np.arange(distogram.shape[0])
#                 y = np.arange(distogram.shape[1])
#                 z = np.arange(distogram.shape[3])
#                 X, Y = np.meshgrid(x, y)
#                 Z = np.zeros_like(X)

#                 for i in range(distogram.shape[0]):
#                     for j in range(distogram.shape[1]):
#                         for k in range(distogram.shape[3]):
#                             if distogram[i, j, idx, k] == 1:
#                                 Z[i, j] = k

#                 # Add a surface for each atom unit measured
#                 fig.add_trace(go.Surface(
#                     z=Z,
#                     x=X,
#                     y=Y,
#                     colorscale=colormaps[idx],  
#                     opacity=0.5,
#                     name=f"Item {idx}",
#                     showscale=False
#                 ))
 
#         case 'float64': #else non bucketized => continuous landscape
            
#             num_atoms=1 if distogram.ndim==2 else distogram.shape[2] #-- number of atoms in distogram
#             if num_atoms==1:
#                 distogram=np.expand_dims(distogram, axis=2) #-- if only one atom, expand the dimensions to make it 3D (better to limit errors)
            
#             for i in range(num_atoms):
#                 data = distogram[:, :, i]
#                 x = np.arange(data.shape[1])
#                 y = np.arange(data.shape[0])
#                 X, Y = np.meshgrid(x, y)

#                 # Add a surface for each slice (atom unit)
#                 fig.add_trace(go.Surface(
#                     z=data,
#                     x=X,
#                     y=Y,
#                     colorscale=colormaps[i],  
#                     showscale=False,  
#                     opacity=0.5,  # set transparency for overlapping slices
#                     name=f"Slice {i}"
#                 ))
#     b = 0 #if distogram.ndim == 4 else distogram.shape[3] 

#     # -- unified layout
#     title_str = '3D vis distogram landscape'
#     if num_atoms > 1:
#         title_str += f' for {num_atoms} stacked plot/atom'
#     if b > 0:
#         title_str += f' (discretized)'
        
#     fig.update_layout(
#         title=title_str,
#         scene=dict(
#             xaxis_title="X-axis residues",
#             yaxis_title="Y-axis residues",
#             zaxis_title="Distance"
#         ),
#         margin=dict(l=10, r=10, t=30, b=10)
#     )
    
#     if plot:
#         fig.show()
#     if save:
#         fig.write_html(f"distogram_{structure_no}_{num_atoms}_{b}.html")

#     return fig

# import numpy as np
# import plotly.graph_objects as go