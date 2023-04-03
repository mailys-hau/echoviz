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
    proot = Path("~/Documents/outputs/test-predictions")
    pinput = Path("~/Documents/data/hdf-isotropic/ref.h5").expanduser()
    pbpred = proot.joinpath("bin.h5").expanduser()
    pmpred = proot.joinpath("multi.h5").expanduser()

    # Additional info for voxel grid
    ih5 = h5py.File(pinput, 'r')
    spacing = ih5["VolumeGeometry"]["resolution"][()]
    origin = ih5["VolumeGeometry"]["origin"][()]
    directions = ih5["VolumeGeometry"]["directions"][()]
    fnb = ih5["VolumeGeometry"]["frameNumber"][()]
    ih5.close()
    pbh5, pmh5 = h5py.File(pbpred, 'r'), h5py.File(pmpred, 'r')
    inputs = []
    anteriors, posteriors, targets = [], [], [] # Annotations
    pralls, prants, prposts = [], [], []
    # Load frames in each category (input, labels, prediction)
    for i in range(1, fnb):
        # Input is identical in both files
        h5vol = pbh5["Input"][f"vol{i:02d}"][()]
        inputs.append(VoxelGrid(h5vol, origin, directions, spacing))
        # Binary segmentation target
        tg = pbh5["Target"][f"vol{i:02d}"][()]
        targets.append(VoxelGrid(tg, origin, directions, spacing))
        # Multi segmantation target
        ant = pmh5["Target"][f"anterior-{i:02d}"][()]
        anteriors.append(VoxelGrid(ant, origin, directions, spacing))
        post = pmh5["Target"][f"posterior-{i:02d}"][()]
        posteriors.append(VoxelGrid(post, origin, directions, spacing))
        # Predictions
        pra = pbh5["Prediction"][f"vol{i:02d}"][()]
        pralls.append(VoxelGrid(pra, origin, directions, spacing))
        prant = pmh5["Prediction"][f"anterior-{i:02d}"][()]
        prpost = pmh5["Prediction"][f"posterior-{i:02d}"][()]
        prants.append(VoxelGrid(prant, origin, directions, spacing))
        prposts.append(VoxelGrid(prpost, origin, directions, spacing))
    pbh5.close(), pmh5.close()
    # Try the plotting
    print("Here's some 2D static plots.")
    _time_plot(plot_slice, inputs[0],
               {"anterior": anteriors[0], "posterior": posteriors[0]},
               120, axis=1, plot_input=False, title="Labels on input")
    _time_plot(plot_slice, inputs[0], {"all": targets[0]},
               120, axis=2, vpreds={"all": pralls[0]}, threshold=0.5,
               filename=POUTS["png"], title="Labels on input & predictions")
    _show_res("image", POUTS["png"])
    print("Now for some 3D static plots.")
    _time_plot(static_3d, inputs[-1],
               {"anterior": anteriors[-1], "posterior": posteriors[-1]},
               vpreds={"anterior": prants[-1], "posterior": prposts[-1]},
               threshold=0.5, filename=POUTS["png"],
               title="Input, labels & predictions")
    _show_res("image", POUTS["png"])
    print("Let's make it fancy and have an interactive 3D plot")
    _time_plot(interactive_3d, inputs[-1],
               {"anterior": anteriors[-1], "posterior": posteriors[-1]},
               show=False, filename=POUTS["html"], title="Input & labels")
    _show_res("web file", POUTS["html"])
    print("Back to 2D! But with a twist... It's animated o/")
    _time_plot(sliced_sequence, inputs,
               {"anterior": anteriors, "posterior": posteriors},
               60, axis=0, filename=POUTS["gif"], title="Input & labels")
    _show_res("gif", POUTS["gif"])
    _time_plot(sliced_volume, inputs[-2], {"all": targets[-2]},
               axis=2, vpreds={"all": pralls[-2]}, plot_input=False,
               filename=POUTS["gif"], title="Labels on input & predictions")
    _show_res("gif", POUTS["gif"])
    print("And for the grand finale... Interactive 3D animated plot!!")
    _time_plot(animated_3d, inputs, None,
               vpreds={"anterior": prants, "posterior": prposts},
               filename=POUTS["html"], title="Input & predictions", show=False)
    _show_res("web file", POUTS["html"])
    sleep(3) # Wait so last file can be seen before being removed
    for p in POUTS.values(): #Remove created files
        p.unlink(missing_ok=True)



if __name__ == "__main__":
    testy_testa()
