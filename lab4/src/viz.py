import plotly.graph_objects as go
import numpy as np

def view_distogram(y_transformed:dict, 
                    structure_no=0, 
                    colormaps=['viridis', 'plasma', 'magma', 'cividis', 'inferno', 'YlGnBu', 'YlOrRd', 'Blues', 'Greens', 'Reds']):
    '''
    takes a dict of y transformations, and viz the distogram through interactive landscape and heatmaps
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

    # -- unified layout
    fig.update_layout(
        title=f"Distogram (3D Visualization of {num_atoms} Slices)",
        scene=dict(
            xaxis_title="X-axis residues",
            yaxis_title="Y-axis residues",
            zaxis_title="Distance"
        ),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    b=None if distogram.ndim==4 else distogram.shape[4]
    print('num_atoms:',num_atoms,'; num_buckets:', b,'; structure_no:',structure_no)
    fig.show()