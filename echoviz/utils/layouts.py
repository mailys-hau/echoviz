LAYOUT_2D = {"title_y": 0.98,
             "autosize": False,
             "height": 350,
             "margin": {'l': 10, 'r': 10, 't': 30, 'b': 10}
             }

NAKED_AXIS = {"showgrid": False, "showticklabels": False}


CAMERA = {"eye": {'x': -0.5, 'y': -1.15, 'z': 0.7},
          "up": {'x': 0, 'y': 0, 'z': 0.5}}

LAYOUT_3D = {"scene_camera": CAMERA,
             "plot_bgcolor": "rgb(64, 64, 64)",
             "title_y": 0.98,
             "autosize": False,
             "width": 600,
             "height": 500,
             "margin": {'l': 10, 't': 30, 'b': 10}
             }


CONTOUR = {"color": "lightgrey", "show": True, "width": 10}


def frame_args(duration):
    return {"frame": {"duration": duration, "redraw": True},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"}}

LAYOUT_4D = {
        "sliders": [{
            "len": 0.8,
            'x': 0.1, 'y': 0
            }],
        "updatemenus": [{
            "buttons": [{
                "args": [None, frame_args(200)],
                "label": "&#9654;", # Play symbol
                "method": "animate"
                },
                {
                "args": [[None], frame_args(0)],
                "label": "&#9724;", # Pause symbol
            "method": "animate"}],
            "direction": "left",
            "type": "buttons",
            'x': 0, 'y': 0
            }],
        }
