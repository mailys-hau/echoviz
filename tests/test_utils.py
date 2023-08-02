import h5py

from datetime import timedelta
from pathlib import Path
import subprocess
from time import sleep, time

from echoviz import VoxelGrid




POUTS = {ext: Path(f"test-output.{ext}").resolve() for ext in ["png", "gif", "html"]}
YES = ['y', "yes", '']



def time_plot(func, inputs, labels, *args, **kwargs):
    start = time()
    func(inputs, labels, *args, **kwargs)
    end = time()
    print(f"    `{func.__name__}` took {timedelta(seconds=(end - start))} to run.")

def show_res(dtype, path):
    sentence = ("      Do you want to see the result from previous test as"
                f" {dtype}? (Y/n) ")
    if input(sentence).lower() in YES:
        #FIXME: Don't assume firefox
        subprocess.call(["firefox", path.as_uri()])


def the_end(msg):
    print(msg)
    sleep(3) # Wait so last file can be seen before being removed
    for p in POUTS.values(): #Remove created files
        p.unlink(missing_ok=True)



def _get_grid(array, origin, directions, spacing):
    # You want to copy in case you change the scale because it's the same for several grids
    return VoxelGrid(array, origin.copy(), directions.copy(), spacing.copy())

def load_file(fname):
    hdf = h5py.File(fname, 'r')
    origin = hdf["VolumeGeometry"]["origin"][()]
    directions = hdf["VolumeGeometry"]["directions"][()]
    spacing  = hdf["VolumeGeometry"]["resolution"][()]
    vinp = []
    vtg, vpr = {"all": [], "anterior": [], "posterior": []}, {"all": [], "anterior": [], "posterior": []}
    multi = False
    for i in range(1, len(hdf["Input"]) + 1):
        vinp.append(_get_grid(hdf["Input"][f"vol{i:02d}"][()], origin, directions, spacing))
        try:
            vtg["all"].append(_get_grid(hdf["Target"][f"vol{i:02d}"][()],origin, directions, spacing))
            vpr["all"].append(_get_grid(hdf["Prediction"][f"vol{i:02d}"][()], origin, directions, spacing))
        except KeyError:
            for k in ["anterior", "posterior"]:
                vtg[k].append(_get_grid(hdf["Target"][f"{k}-{i:02d}"][()], origin, directions, spacing))
                vpr[k].append(_get_grid(hdf["Prediction"][f"{k}-{i:02d}"][()], origin, directions, spacing))
            multi = True
    hdf.close()
    if multi: # Clean created directories
        vtg.pop("all"), vpr.pop("all")
    else:
        vtg.pop("anterior"), vtg.pop("posterior")
        vpr.pop("anterior"), vpr.pop("posterior")
    if len(vinp) == 1: # Flatten if only one frame
        vinp = vinp[0]
        for k in vtg.keys():
            vtg[k] = vtg[k][0]
            vpr[k] = vpr[k][0]
    return vinp, vtg, vpr

