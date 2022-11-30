import numpy as np
import plotly.express.colors as pxc



def rgb2rgba(rgb_cmap, min_transparency=0.1, max_transparency=0.7):
    """ Convert RGB scale to RGBA """
    a_cmap = np.linspace(min_transparency, max_transparency, len(rgb_cmap))
    rgba_cmap = []
    for c, a in zip(rgb_cmap, a_cmap):
        cl = c.strip("rgb()").split(',')
        rgba_cmap.append(f"rgba({cl[0]},{cl[1]},{cl[2]},{a})")
    return rgba_cmap



BIN_CMAPS = {"anterior": rgb2rgba(["rgb(145,53,125)"] * 2, 0),
             "posterior": rgb2rgba(["rgb(8,81,156)"] * 2, 0),
             "all": rgb2rgba(["rgb(153,52,4)"] * 2, 0)}
HEAT_CMAPS = {"anterior": rgb2rgba(pxc.sequential.Magenta),
              "posterior": rgb2rgba(pxc.sequential.Blues),
              "all": rgb2rgba(pxc.sequential.YlOrBr)}
