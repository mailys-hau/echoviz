"""
3D plot of mitral valve voxels from voxel grids (see `utils/voxel_grid.py`)
Functions are adaptated from: https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/
"""

import numpy as np
import plotly.graph_objects as go

from plotly.offline import iplot
from warnings import warn

from utils import BIN_CMAPS, HEAT_CMAPS



def _make_plotly_mesh(voxels, level=None, mask=False, stride=1, **kwargs):
    verts, faces, values = voxels.devoxelize(level, mask, stride)
    x, y, z = zip(*verts)
    i, j, k = zip(*faces)
    intensity = None if "color" in kwargs else values
    return go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, intensity=intensity, **kwargs)

def interactive_3d(vinput, vlabels=None, vpreds=None,  mode="hmap",
                   title="", show=True, filename=None):
    """
    """
    #FIXME? Add classes legend
    if vlabels and vpreds:
        warn("Plotting label and annotation in 3D make for a busy plot", UserWarning)
    camera = {"eye": {'x': -0.50, 'y': -1.15, 'z': 0.70},
              "up": {'x': 0, 'y': 0, 'z': 0.50}}
    inp_mesh = _make_plotly_mesh(vinput, level=50, stride=6, showscale=False,
                                 opacity=0.3, colorscale="ice", reversescale=True)
    fig = go.Figure(data=inp_mesh)
    fig.update_layout(scene_camera=camera, title=title, title_y=0.98,
                      plot_bgcolor="rgb(64, 64, 64)",
                      autosize=False, width=600, height=500, margin=dict(l=10, t=30, b=10))
    if vlabels:
        lab_meshes = []
        for k in vlabels.keys():
            lab_meshes.append(_make_plotly_mesh(vlabels[k], stride=2,
                                                color=BIN_CMAPS[k][1]))
        fig.add_traces(lab_meshes)
    if vpreds:
        pred_meshes = []
        for k in vpreds.keys():
            if mode == "hmap":
                pred_meshes.append(_make_plotly_mesh(vpreds[k], stride=2,
                                                     colorscale=HEAT_CMAPS[k]))
            elif mode == "bmap":
                pred_meshes.append(_make_plotly_mesh(vpreds[k].float2bool(), stride=2,
                                                     color=BIN_CMAPS[k][1]))
            else:
                raise ValueError("Invalid plot mode. It can be `hmap` or `bmap`.")
        fig.add_traces(pred_meshes)
    if show:
        iplot(fig)
    if filename:
        #FIXME: Diminish file size by removing js modules
        if filename.suffix != ".html":
            filename = filename.with_suffix(".html")
        fig.write_html(filename)
    return fig
