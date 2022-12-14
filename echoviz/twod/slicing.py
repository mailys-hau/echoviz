"""
Plot specific slice of 3D volume for better understanding of data
"""

import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go

from plotly.offline import iplot
from plotly.subplots import make_subplots

from echoviz.utils import BIN_CMAPS, HEAT_CMAPS



def _rot_slice(voxel_grid, key):
    return np.rot90(voxel_grid.values[key])


def plot_slice(vinput, vlabels, index, axis=1, vpreds=None, threshold=None,
               plot_input=True, title='', show=True, filename=None):
    # Expect vinput and vlabel to be VoxelGrid
    key = [slice(None), slice(None), slice(None)]
    key[axis] = index
    key = tuple(key)
    # Get them sliced
    sinput = _rot_slice(vinput, key)
    slabels = {k: _rot_slice(v, key).astype(np.uint8) for k, v in vlabels.items()}
    nb_col = (2 if vpreds else 1) + plot_input
    fig = make_subplots(cols=nb_col, horizontal_spacing=0.01)
    for c in range(nb_col):
        fig.add_trace(go.Heatmap(z=sinput, colorscale="Greys_r"), col=c+1, row=1)
    # Groundtruth
    for k in slabels.keys():
        fig.add_trace(go.Heatmap(z=slabels[k], colorscale=BIN_CMAPS[k]),
                      col=min(nb_col, 2), row=1)
    if vpreds:
        cmaps = BIN_CMAPS if threshold else HEAT_CMAPS
        for k in vpreds.keys():
            pred = np.rot90(vpreds[k].float2bool(threshold).values[key]) \
                    if threshold else _rot_slice(vpreds[k], key)
            fig.add_trace(go.Heatmap(z=pred, colorscale=cmaps[k]),
                          col=nb_col, row=1)
    fig.update_layout(title=title, autosize=False, margin=dict(l=10, r=10, t=30, b=10),
                      width=nb_col*350, height=350, title_y=0.98)
    fig.update_xaxes(showgrid=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, showticklabels=False)
    fig.update_traces(showscale=False)
    if show:
        iplot(fig)
    if filename:
        #FIXME: Make file lighter
        fig.write_image(filename, format=filename.suffix.strip('.'))
    return fig
