import plotly.graph_objects as go

from plotly.offline import iplot
from pysdf import SDF
from warnings import warn

from echoviz.utils.colors import BIN_CMAPS, HEAT_CMAPS
from echoviz.utils.layouts import LAYOUT_3D, LAYOUT_4D, CONTOUR, frame_args
from echoviz.utils.misc import clean_fname



def animated_3d(vinputs, vlabels=None, vpreds=None, threshold=None,
                title="", show=True, filename=None):
    frames = []
    #TODO: Multithread this
    for i in range(len(vinputs)):
        data = [vinputs[i].make_mesh(opacity=0.3, showscale=False, colorscale="Greys", cmin=0, cmax=1)]
        if vlabels:
            for k in vlabels.keys():
                try:
                    data.append(vlabels[k][i].make_mesh(color=BIN_CMAPS[k][1]))
                except RuntimeError:
                    warn(f"{k.capitalize()} label for frame {i} is null, not plotting it.", RuntimeWarning)
        if vpreds:
            for k in vpreds.keys():
                try:
                    if threshold:
                        data.append(vpreds[k][i].float2bool(threshold)
                                                .make_mesh(color=BIN_CMAPS[k][1]))
                    else:
                        data.append(vpreds[k][i].make_mesh(colorscale=HEAT_CMAPS[k], cmin=0, cmax=1))
                except RuntimeError:
                    warn(f"{k.capitalize()} prediction for frame {i} is null, not plotting it.", RuntimeWarning)
        frames.append(go.Frame(data=data, name=str(i)))
    layout = LAYOUT_4D
    layout["sliders"][0]["steps"] = [{
        "args": [[str(i)], frame_args(0)],
        "label": str(i),
        "method": "animate",
        } for i in range(len(frames)) ]
    #FIXME: fix range to smooth animation
    fig = go.Figure(data=frames[0].data, frames=frames, layout=layout)
                    #range_x=[], range_y=[], range_z=[])
    fig.update_layout(title=title, **LAYOUT_3D)
    fig.update_traces(showscale=False)
    if show:
        iplot(fig)
    if filename:
        filename = clean_fname(filename)
        fig.write_html(filename) #FIXME: Reduce file size
    return fig



def _dist_4d(vlabels, vpreds, fdist, vinputs=None,
             title='', colorscale="delta", show=True, filename=None):
    frames = []
    cmin, cmax = 10000, -10000
    nbf = len(list(vlabels.values())[0])
    #TODO: Multithread this
    for i in range(nbf):
        data = []
        if vinputs:
            data.append(vinputs[i].make_mesh(opacity=0.3, showscale=False, colorscale="Greys", cmin=0, cmax=1))
        for k in vlabels.keys():
            try:
                verts, faces, _ = vlabels[k][i].devoxelize()
            except RuntimeError:
                warn(f"{k.capitalize()} label for frame {i} is null, not plotting it.", RuntimeWarning)
            sdf = SDF(verts, faces)
            try:
                verts, faces, _ = vpreds[k][i].devoxelize()
            except RuntimeError:
                warn(f"{k.capitalize()} prediction for frame {i} is null, not plotting it.", RuntimeWarning)
            sdf_res = fdist(sdf(verts))
            cmin, cmax = min(min(sdf_res), cmin), max(max(sdf_res), cmax)
            data.append(vpreds[k][i].make_mesh(verts=verts, faces=faces, values=sdf_res, name=k,
                                               opacity=0.7, colorscale=colorscale, contour=CONTOUR))
        frames.append(go.Frame(data=data, name=str(i)))
    layout = LAYOUT_4D
    layout["sliders"][0]["steps"] = [{
        "args": [[str(i)], frame_args(0)],
        "label": str(i),
        "method": "animate",
        } for i in range(len(frames)) ]
    #FIXME: fix range to smooth animation
    fig = go.Figure(data=frames[0].data, frames=frames, layout=layout)
                    #range_x=[], range_y=[], range_z=[])
    fig.update_layout(title=title, **LAYOUT_3D)
    traces = {"cmin": cmin, "cmax": cmax, "showscale": True}
    if cmin < 0 and cmax > 0:
        traces["cmid"] = 0
    fig.update_traces(traces, lambda t: t.name != "input")
    if show:
        iplot(fig)
    if filename:
        filename = clean_fname(filename)
        fig.write_html(filename) #FIXME: Reduce file size
    return fig


def sdf_animated_3d(vlabels, vpreds, vinputs=None, title='', show=True, filename=None):
    return _dist_4d(vlabels, vpreds, lambda x: x, vinputs=vinputs, title=title,
                    show=show, filename=filename)

def asd_animated_3d(vlabels, vpreds, vinputs=None, title='', show=True, filename=None):
    return _dist_4d(vlabels, vpreds, lambda x: abs(x), vinputs=vinputs, title=title,
                    colorscale="viridis_r", show=show, filename=filename)
