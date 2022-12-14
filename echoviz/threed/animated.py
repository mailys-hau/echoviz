import plotly.graph_objects as go

from plotly.offline import iplot

from echoviz.utils import BIN_CMAPS, HEAT_CMAPS

#TODO: 3D "annimation", add slider for frames
#TODO: gif making for sliced plot (3D would be hard to read)



def _frame_args(duration):
    return {"frame": {"duration": duration, "redraw": True},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"}}


def animated_3d(vinputs, vlabels=None, vpreds=None, threshold=None,
                title="", show=True, filename=None):
    frames = []
    #TODO: Multithread this
    for i in range(len(vinputs)):
        data = [vinputs[i].make_mesh(level=50, stride=6, opacity=0.3,
                                     showscale=False, colorscale="ice",
                                     reversescale=True)]
        if vlabels:
            for k in vlabels.keys():
                data.append(vlabels[k][i].make_mesh(stride=2, color=BIN_CMAPS[k][1]))
        if vpreds:
            for k in vpreds.keys():
                if threshold:
                    data.append(vpreds[k][i].float2bool(threshold)
                                            .make_mesh(stride=2, color=BIN_CMAPS[k][1]))
                else:
                    data.append(vpreds[k][i].make_mesh(stride=2, colorscale=HEAT_CMAPS[k]))
        frames.append(go.Frame(data=data, name=str(i)))
    layout = {"sliders": [{
                "len": 0.8,
                'x': 0.1, 'y': 0,
                "steps": [{
                    "args": [[str(i)], _frame_args(0)],
                    "label": str(i),
                    "method": "animate",
                  } for i in range(len(frames))]}],
              "updatemenus": [{
                  "buttons": [{"args": [None, _frame_args(200)],
                               "label": "&#9654;", # Play symbol
                               "method": "animate"},
                              {"args": [[None], _frame_args(0)],
                               "label": "&#9724;", # Pause symbol
                               "method": "animate"}],
                  "direction": "left",
                  "type": "buttons",
                  'x': 0, 'y': 0
                }],
             }
    #FIXME: fix range to smooth animation
    fig = go.Figure(data=frames[0].data, frames=frames, layout=layout)
                    #range_x=[], range_y=[], range_z=[])
    camera = {"eye": {'x': -0.5, 'y': -1.15, 'z': 0.7},
              "up": {'x': 0, 'y': 0, 'z': 0.5}}
    fig.update_layout(scene_camera=camera, title=title, title_y=0.98,
                      plot_bgcolor="rgb(64,64,64)", autosize=False, width=600,
                      height=500, margin=dict(l=10, t=30, b=10))
    if show:
        iplot(fig)
    if filename:
        filename = filename.with_suffix(".html") if filename.suffix != ".html" else filename
        fig.write_html(filename) #FIXME: Reduce file size
    return frames
