import plotly.graph_objects as go

from pathlib import Path
from plotly.offline import iplot
from pysdf import SDF

from echoviz.utils.colors import SJET_R



def sdf_interactive_3d(vlabels, vpreds, vinputs=None, title='', show=True, filename=None):
    """
    """
    # Create fancy figure
    camera = {"eye": {'x': -0.5, 'y': -1.15, 'z': 0.7},
              "up": {'x': 0, 'y': 0, 'z': 0.5}}
    layout = dict(scene_camera=camera, title=title, title_y=0.98, plot_bgcolor="rgb(64, 64, 64)",
                  autosize=False, width=600, height=500, margin=dict(l=10, t=30, b=10))
    fig = go.Figure(layout=layout)
    if vinputs:
        fig.add_trace(vinputs.make_mesh(showscale=False, opacity=0.3, colorscale="Greys", cmin=0, cmax=1, name="input"))
    cmin, cmax = 10000, -10000
    for k in vlabels.keys():
        verts, faces, _ = vlabels[k].devoxelize()
        sdf = SDF(verts, faces)
        verts, faces, _ = vpreds[k].devoxelize()
        sdf_res = sdf(verts)
        cmin, cmax = min(min(sdf_res), cmin), max(max(sdf_res), cmax)
        fig.add_trace(vpreds[k].make_mesh(verts=verts, faces=faces, values=sdf_res, opacity=0.7, contour={"color": "lightgrey", "show": True, "width": 10},
                                          cmin=cmin, cmax=cmax, name=k, colorscale=SJET_R))
    # Homogenize SDF colorscale
    fig.update_traces({"cmin": cmin, "cmax": cmax}, lambda t: t.name != "input")
    if show:
        iplot(fig)
    if filename:
        filename = Path(filename)
        #FIXME: Diminish file size by removing js modules
        if filename.suffix != ".html":
            filename = filename.with_suffix(".html")
        fig.write_html(filename)
    return fig
