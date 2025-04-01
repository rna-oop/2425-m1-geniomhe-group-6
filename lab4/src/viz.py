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

def view_distogram(y_transformed:dict, 
                    structure_no=0, 
                    colormaps=['viridis', 'plasma', 'magma', 'cividis', 'inferno', 'YlGnBu', 'YlOrRd', 'Blues', 'Greens', 'Reds'],
                    plot=True,
                    save=False):
    '''
    takes a dict of y transformations, and viz the distogram through interactive landscape and heatmaps
    
    parameters:
    - y_transformed: dict of y transformations (works also on the distograms saved in ndarray)
    - structure_no: index of the structure to visualize (default is 0)
    - colormaps: list of colormaps to use for the distogram (default is a list of 10 colormaps)
    - plot: boolean to show the figure (default is True)
    - save: boolean to save the figure as html (default is False)

    returns:
    - fig (plotly figure): interactive distogram visualization
    
    '''
    if isinstance(y_transformed,dict): #temp for testing
        y_transformed=y_transformed['Distogram'] #

    fig = go.Figure()
    colormaps=['viridis', 'plasma', 'magma', 'cividis', 'inferno', 'YlGnBu', 'YlOrRd', 'Blues', 'Greens', 'Reds']
    distogram=y_transformed[0]

    match y_transformed.dtype:
        case 'int64': #if bucketized => discrete landscape

            if distogram.ndim==3:
                # -- expand 3rd dim to be 1 (limits errors)
                distogram=np.expand_dims(distogram, axis=2)

            num_atoms=distogram.shape[2] #-- number of atoms in distogram

            for idx in range(distogram.shape[2]):
                x = np.arange(distogram.shape[0])
                y = np.arange(distogram.shape[1])
                z = np.arange(distogram.shape[3])
                X, Y = np.meshgrid(x, y)
                Z = np.zeros_like(X)

                for i in range(distogram.shape[0]):
                    for j in range(distogram.shape[1]):
                        for k in range(distogram.shape[3]):
                            if distogram[i, j, idx, k] == 1:
                                Z[i, j] = k

                # Add a surface for each atom unit measured
                fig.add_trace(go.Surface(
                    z=Z,
                    x=X,
                    y=Y,
                    colorscale=colormaps[idx],  
                    opacity=0.5,
                    name=f"Item {idx}",
                    showscale=False
                ))
 
        case 'float64': #else non bucketized => continuous landscape
            
            num_atoms=1 if distogram.ndim==2 else distogram.shape[2] #-- number of atoms in distogram
            if num_atoms==1:
                distogram=np.expand_dims(distogram, axis=2) #-- if only one atom, expand the dimensions to make it 3D (better to limit errors)
            
            for i in range(num_atoms):
                data = distogram[:, :, i]
                x = np.arange(data.shape[1])
                y = np.arange(data.shape[0])
                X, Y = np.meshgrid(x, y)

                # Add a surface for each slice (atom unit)
                fig.add_trace(go.Surface(
                    z=data,
                    x=X,
                    y=Y,
                    colorscale=colormaps[i],  
                    showscale=False,  
                    opacity=0.5,  # set transparency for overlapping slices
                    name=f"Slice {i}"
                ))
    b = 0 #if distogram.ndim == 4 else distogram.shape[3] 

    # -- unified layout
    title_str = '3D vis distogram landscape'
    if num_atoms > 1:
        title_str += f' for {num_atoms} stacked plot/atom'
    if b > 0:
        title_str += f' (discretized)'
        
    fig.update_layout(
        title=title_str,
        scene=dict(
            xaxis_title="X-axis residues",
            yaxis_title="Y-axis residues",
            zaxis_title="Distance"
        ),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    
    if plot:
        fig.show()
    if save:
        fig.write_html(f"distogram_{structure_no}_{num_atoms}_{b}.html")

    return fig



def view_one_hot(X, structure_no=0,width=None,height=None,y_ticks=False,plot=True,save=False):
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

    returns:
    - fig (plotly figure): heatmap of the one-hot encoded matrix

    """
    data=X[structure_no]

    alphabet=['A','C','U','G']
    k=int(math.log2(X.shape[2])/math.log2(4))
    all_kmers_comb_reconstructed =["".join(i) for i in product(alphabet, repeat=k)]
    
    col_names = all_kmers_comb_reconstructed
    row_names = [f"{i+1}" for i in range(data.shape[0])]

    fig = go.Figure(data=go.Heatmap(
        z=data,
        colorscale=[[0, 'white'], [1, 'black']],  # White for 0, Black for 1
        showscale=False
    ))

    cell_size = 70  # Adjust this value for larger/smaller squares

    # Calculate the figure size dynamically
    if width is not None:
        fig_width = width
    else:
        fig_width = cell_size * len(col_names)

    if height is not None:
        fig_height = height
    else:
        fig_height = int(cell_size * len(row_names) * 0.45 )

    # Update layout
    fig.update_layout(
        height=fig_height,
        width=fig_width,
        title="Binary Matrix Visualization",
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(col_names))),
            ticktext=col_names
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

    if save:
        # saves as html
        fig.write_html(f"one_hot_{structure_no}.html")
        
    return fig
