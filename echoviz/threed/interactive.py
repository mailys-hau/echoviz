"""
3D plot of mitral valve voxels from voxel grids (see `utils/voxel_grid.py`)
Functions are adaptated from: https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/
"""

import numpy as np
import plotly.graph_objects as go

from plotly.offline import iplot
from warnings import warn

from echoviz.utils import BIN_CMAPS, HEAT_CMAPS



def interactive_3d(vinput, vlabels=None, vpreds=None, threshold=None,
                   title="", show=True, filename=None):
    """
    """
    #FIXME? Add classes legend
    if vlabels and vpreds:
        warn("Plotting label and annotation in 3D make for a busy plot", UserWarning)
    camera = {"eye": {'x': -0.5, 'y': -1.15, 'z': 0.7},
              "up": {'x': 0, 'y': 0, 'z': 0.5}}
    inp_mesh = vinput.make_mesh(level=50, stride=6, showscale=False,
                                 opacity=0.3, colorscale="ice", reversescale=True)
    fig = go.Figure(data=inp_mesh)
    fig.update_layout(scene_camera=camera, title=title, title_y=0.98,
                      plot_bgcolor="rgb(64, 64, 64)",
                      autosize=False, width=600, height=500, margin=dict(l=10, t=30, b=10))
    if vlabels:
        lab_meshes = []
        for k in vlabels.keys():
            lab_meshes.append(vlabels[k].make_mesh(stride=2, color=BIN_CMAPS[k][1]))
        fig.add_traces(lab_meshes)
    if vpreds:
        pred_meshes = []
        for k in vpreds.keys():
            if threshold:
                pred_meshes.append(vpreds[k].float2bool(threshold)
                                            .make_mesh(stride=2, color=BIN_CMAPS[k][1]))
            else:
                pred_meshes.append(vpreds[k].make_mesh(stride=2, colorscale=HEAT_CMAPS[k]))
        fig.add_traces(pred_meshes)
    if show:
        iplot(fig)
    if filename:
        #FIXME: Diminish file size by removing js modules
        if filename.suffix != ".html":
            filename = filename.with_suffix(".html")
        fig.write_html(filename)
    return fig
