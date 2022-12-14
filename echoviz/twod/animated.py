from io import BytesIO
from plotly.offline import iplot
from PIL import Image

from echoviz.twod.slicing import plot_slice



def _get_frame(data, idx):
    if data:
        return {k: data[k][idx] for k in data.keys()}
    return None


def sliced_sequence(vinputs, vlabels, index, axis=1, vpreds=None, threshold=None,
                   plot_input=True, title='', filename=None):
    imgs = []
    for f, vinp in enumerate(vinputs): #FIXME: Multithread to optimize time
        vlab, vpred = _get_frame(vlabels, f), _get_frame(vpreds, f)
        fig = plot_slice(vinp, vlab, index, axis, vpred, threshold,
                         plot_input, title, show=False, filename=None)
        img_str = fig.to_image(format="png")
        imgs.append(Image.open(BytesIO(img_str)))
    filename = filename if filename else "sliced_sequence.gif"
    with open(filename, "wb") as fd:
        imgs[0].save(fd, save_all=True, append_images=imgs[1:],
                     optimize=True, duration=100, loop=0)


def sliced_volume(vinput, vlabels, axis=1, vpreds=None, threshold=None,
                  stride=10, plot_input=True, title='', filename=None):
    imgs = []
    max_index = vinput.shape[axis]
    #FIXME: Multithread to optimize time
    for index in range(0, max_index, stride):
        fig = plot_slice(vinput, vlabels, index, axis, vpreds, threshold,
                         plot_input, title, show=False, filename=None)
        img_str = fig.to_image(format="png")
        imgs.append(Image.open(BytesIO(img_str)))
    filename = filename if filename else "sliced_volume.gif"
    with open(filename, "wb") as fd:
        imgs[0].save(fd, save_all=True, append_images=imgs[1:],
                     optimize=True, duration=150, loop=0)
