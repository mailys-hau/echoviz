"""
3D plot of mitral valve voxels from voxel grids (see `utils/voxel_grid.py`)
"""

import plotly.express as px

from io import BytesIO
from PIL import Image

from echoviz.threed.interactive import interactive_3d



def static_3d(vinput, vlabels=None, vpreds=None, threshold=None,
              title="", show=True, filename=None):
    fig = interactive_3d(vinput, vlabels, vpreds, threshold, title, show=False)
    extension = filename.suffix.strip('.') if filename else "png"
    img_str = fig.to_image(format=extension)
    if show:
        img = Image.open(BytesIO(img_str))
        fig = px.imshow(img)
        fig.update_layout(autosize=False, width=600, height=500,
                          margin=dict(l=0, t=0, r=0, b=0))
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig.show()
    if filename:
        with open(filename, "wb") as fd:
            fd.write(img_str)
