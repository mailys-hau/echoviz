"""
3D plot of mitral valve voxels from voxel grids (see `utils/voxel_grid.py`)
Functions are adaptated from: https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/
"""

import numpy as np
import plotly.graph_objects as go

from plotly.offline import iplot
from warnings import warn

from echoviz.utils import BIN_CMAPS, HEAT_CMAPS
from echoviz.utils.layouts import LAYOUT_3D
from echoviz.utils.misc import clean_fname



def interactive_3d(vinput, vlabels=None, vpreds=None, threshold=None,
                   title="", show=True, filename=None):
    """
    """
    #FIXME? Add classes legend
    #FIXME: Make vinput optional
    if vlabels and vpreds:
        warn("Plotting label and annotation in 3D make for a busy plot", UserWarning)
    inp_mesh = vinput.make_mesh(showscale=False, opacity=0.3, colorscale="Greys", cmin=0, cmax=1)
    fig = go.Figure(data=inp_mesh, layout=dict(title=title, **LAYOUT_3D))
    if vlabels:
        lab_meshes = []
        for k in vlabels.keys():
            try:
                lab_meshes.append(vlabels[k].make_mesh(color=BIN_CMAPS[k][1]))
            except RuntimeError:
                warn(f"{k.capitalize()} label is null, not plotting it.", RuntimeWarning)
        fig.add_traces(lab_meshes)
    if vpreds:
        pred_meshes = []
        for k in vpreds.keys():
            try:
                if threshold:
                    pred_meshes.append(vpreds[k].float2bool(threshold)
                                                .make_mesh(color=BIN_CMAPS[k][1]))
                else:
                    pred_meshes.append(vpreds[k].make_mesh(colorscale=HEAT_CMAPS[k], cmin=0, cmax=1))
            except RuntimeError:
                warn(f"{k.capitalize()} prediction is null, not plotting it.", RuntimeWarning)
        fig.add_traces(pred_meshes)
        fig.update_traces(showscale=False)
    if show:
        iplot(fig)
    if filename:
        filename = clean_fname(filename)
        #FIXME: Diminish file size by removing js modules
        fig.write_html(filename)
    return fig
