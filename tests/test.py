import h5py

from datetime import timedelta
from pathlib import Path
import subprocess
from time import sleep, time


from echoviz import (animated_3d, interactive_3d, static_3d,
                     plot_slice, sliced_sequence, sliced_volume,
                     VoxelGrid)




POUTS = {ext: Path(f"test-output.{ext}").resolve() for ext in ["png", "gif", "html"]}
YES = ['y', "yes", '']



def _time_plot(func, inputs, labels, *args, **kwargs):
    start = time()
    func(inputs, labels, *args, **kwargs)
    end = time()
    print(f"    `{func.__name__}` took {timedelta(seconds=(end - start))} to run.")

def _show_res(dtype, path):
    sentence = ("      Do you want to see the result from previous test as"
                f" {dtype}? (Y/n)")
    if input(sentence).lower() in YES:
        #FIXME: Don't assume firefox
        subprocess.call(["firefox", path.as_uri()])


def testy_testa():
    # Files to plot
    pinput = Path("~/Documents/data/GE_subset/20150624151535_FMR.h5").expanduser()
    ppred = Path("~/Documents/outputs/3dmv-segmentation/equi-loss/20150624151535_FMR.h5").expanduser()

    ih5, ph5 = h5py.File(pinput, 'r'), h5py.File(ppred, 'r')
    # Additional info for voxel grid
    spacing = ih5["ImageGeometry"]["voxelsize"][()]
    origin = ih5["ImageGeometry"]["origin"][()]
    directions = ih5["ImageGeometry"]["directions"][()]
    fnb = ih5["ImageGeometry"]["frameNumber"][()]
    inputs = []
    anteriors, posteriors = [], [] # Annotations
    predictions = []
    # Load frames in each category (input, labels, prediction)
    for i in range(1, fnb):
        h5vol = ih5["CartesianVolumes"][f"vol{i:02d}"][()]
        inputs.append(VoxelGrid(h5vol, origin, directions, spacing))
        ant = ih5["Labels"][f"ant{i:02d}"][()]
        anteriors.append(VoxelGrid(ant, origin, directions, spacing))
        post = ih5["Labels"][f"post{i:02d}"][()]
        posteriors.append(VoxelGrid(post, origin, directions, spacing))
        pred = ph5["Predictions"][f"vol{i:02d}"][()]
        predictions.append(VoxelGrid(pred, origin, directions, spacing))
    ih5.close(), ph5.close()
    # Try the plotting
    print("Here's some 2D static plots.")
    _time_plot(plot_slice, inputs[0],
               {"anterior": anteriors[0], "posterior": posteriors[0]},
               120, axis=1, plot_input=False, title="Labels on input")
    _time_plot(plot_slice, inputs[0],
               {"anterior": anteriors[0], "posterior": posteriors[0]},
               120, axis=2, vpreds={"all": predictions[0]}, threshold=0.5,
               filename=POUTS["png"], title="Labels on input & predictions")
    _show_res("image", POUTS["png"])
    print("Now for some 3D static plots.")
    _time_plot(static_3d, inputs[-1],
               {"anterior": anteriors[-1], "posterior": posteriors[-1]},
               vpreds={"all": predictions[-1]}, threshold=0.5,
               filename=POUTS["png"], title="Input, labels & predictions")
    _show_res("image", POUTS["png"])
    print("Let's make it fancy and have an interactive 3D plot")
    _time_plot(interactive_3d, inputs[-1],
               {"anterior": anteriors[-1], "posterior": posteriors[-1]},
               show=False, filename=POUTS["html"], title="Input & labels")
    _show_res("web file", POUTS["html"])
    print("Back to 2D! But with a twist... It's animated o/")
    _time_plot(sliced_sequence, inputs,
               {"anterior": anteriors, "posterior": posteriors},
               120, filename=POUTS["gif"], title="Input & labels")
    _show_res("gif", POUTS["gif"])
    _time_plot(sliced_volume, inputs[-2],
               {"anterior": anteriors[-2], "posterior": posteriors[-2]},
               axis=2, vpreds={"all": predictions[-2]}, plot_input=False,
               filename=POUTS["gif"], title="Labels on input & predictions")
    _show_res("gif", POUTS["gif"])
    print("And for the grand finale... Interactive 3D animated plot!!")
    _time_plot(animated_3d, inputs, None, vpreds={"all": predictions},
               filename=POUTS["html"], title="Input & predictions", show=False)
    _show_res("web file", POUTS["html"])
    sleep(3) # Wait so last file can be seen before being removed
    for p in POUTS.values(): #Remove created files
        p.unlink(missing_ok=True)



if __name__ == "__main__":
    testy_testa()
