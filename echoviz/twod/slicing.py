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
from echoviz.utils.layouts import LAYOUT_2D, NAKED_AXIS
from echoviz.utils.misc import clean_fname



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
        fig.add_trace(go.Heatmap(z=sinput, colorscale="Greys_r", zmin=0, zmax=1), col=c+1, row=1)
    # Groundtruth
    for k in slabels.keys():
        fig.add_trace(go.Heatmap(z=slabels[k], colorscale=BIN_CMAPS[k], zmin=0, zmax=1),
                      col=min(nb_col, 2), row=1)
    if vpreds:
        cmaps = BIN_CMAPS if threshold else HEAT_CMAPS
        for k in vpreds.keys():
            pred = np.rot90(vpreds[k].float2bool(threshold).values[key]) \
                    if threshold else _rot_slice(vpreds[k], key)
            fig.add_trace(go.Heatmap(z=pred, colorscale=cmaps[k], zmin=0, zmax=1),
                          col=nb_col, row=1)
    fig.update_layout(title=title, width=nb_col*350, **LAYOUT_2D)
    fig.update_xaxes(**NAKED_AXIS), fig.update_yaxes(**NAKED_AXIS)
    fig.update_traces(showscale=False)
    if show:
        iplot(fig)
    if filename:
        filename = clean_fname(filename, ".png")
        #FIXME: Make file lighter
        fig.write_image(filename, format=filename.suffix.strip('.'))
    return fig
