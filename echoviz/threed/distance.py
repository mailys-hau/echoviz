import plotly.graph_objects as go

from plotly.offline import iplot
from pysdf import SDF
from warnings import warn

from echoviz.utils.layouts import LAYOUT_3D, CONTOUR
from echoviz.utils.misc import clean_fname



def _dist_interactive_3d(vlabels, vpreds, fdist, vinputs=None,
                         title='', colorscale="delta", show=True, filename=None):
    """
    """
    # Create fancy figure
    fig = go.Figure(layout=dict(title=title, **LAYOUT_3D))
    if vinputs:
        fig.add_trace(vinputs.make_mesh(showscale=False, name="input", opacity=0.3,
                                        colorscale="Greys", cmin=0, cmax=1))
    cmin, cmax = 10000, -10000
    for k in vlabels.keys():
        try:
            verts, faces, _ = vlabels[k].devoxelize()
        except RuntimeError:
            warn(f"{k.capitalize()} label is null, not plotting it.", RuntimeWarning)
        sdf = SDF(verts, faces)
        try:
            verts, faces, _ = vpreds[k].devoxelize()
        except RuntimeError:
            warn(f"{k.capitalize()} prediction is null, not plotting it.", RuntimeWarning)
        sdf_res = fdist(sdf(verts))
        cmin, cmax = min(min(sdf_res), cmin), max(max(sdf_res), cmax)
        mesh = vpreds[k].make_mesh(verts=verts, faces=faces, values=sdf_res, name=k,
                                   opacity=0.7, colorscale=colorscale, contour=CONTOUR)
        fig.add_trace(mesh)
    # Homogenize SDF colorscale
    traces = {"cmin": cmin, "cmax": cmax}
    if cmin < 0 and cmax > 0:
        traces["cmid"] = 0
    fig.update_traces(traces, lambda t: t.name != "input")
    if show:
        iplot(fig)
    if filename:
        filename = clean_fname(filename)
        #FIXME: Diminish file size by removing js modules
        fig.write_html(filename)
    return fig


def sdf_interactive_3d(vlabels, vpreds, vinputs=None, title='', show=True, filename=None):
    return _dist_interactive_3d(vlabels, vpreds, lambda x: x, vinputs=vinputs,
                                title=title, show=show, filename=filename)

def asd_interactive_3d(vlabels, vpreds, vinputs=None, title='', show=True, filename=None):
    return _dist_interactive_3d(vlabels, vpreds, lambda x: abs(x), vinputs=vinputs,
                                title=title, colorscale="viridis_r", show=show, filename=filename)
