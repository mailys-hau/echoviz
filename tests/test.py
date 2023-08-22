import click as cli
import echoviz as ecv
import random as rd
import signal
import sys

from pathlib import Path

from test_utils import *




signal.signal(signal.SIGINT, lambda *args: (the_end("\nOk byye."), sys.exit(0)))



@cli.command(context_settings={"help_option_names": ["-h", "--help"], "show_default": True})
@cli.argument("fname", type=cli.Path(exists=True, resolve_path=True, path_type=Path, file_okay=True))
def testy_testa(fname):
    vinp, vtg, vpr = load_file(fname)
    if not isinstance(vinp, list):
        print("The given file is not a sequence, so I'll only test plot that runs on one frame.")
        frame = 1
        bvinp, bvtg, bvpr = vinp, vtg, vpr
    else:
        frame = rd.randint(0, len(vinp) - 1)
        bvinp = vinp[frame]
        bvtg, bvpr = { k: vtg[k][frame] for k in vtg.keys() }, { k: vpr[k][frame] for k in vpr.keys() }
    print(f"We're studying file {fname.name} at frame {frame}.")
    print("Let's start with some 2D static plots.")
    time_plot(ecv.plot_slice, bvinp, bvtg, 64, axis=1, plot_input=False, title="Labels on input")
    time_plot(ecv.plot_slice, bvinp, bvtg, 64, axis=0, vpreds=bvpr, threshold=0.5,
              filename=POUTS["png"], title="Labels on input & predictions")
    show_res("image", POUTS["png"])
    print("Now for some 3D static plots.")
    time_plot(ecv.static_3d, bvinp, bvtg, vpreds=bvpr, threshold=0.5,
              filename=POUTS["png"], title="Input, labels & predictions")
    show_res("image", POUTS["png"])
    # SDF (m)
    time_plot(ecv.sdf_static_3d, bvtg, bvpr, vinputs=bvinp, title="SDF (m)")
    # ASD (m)
    bvinp.set_scale('m')
    for k in bvtg.keys():
        bvtg[k].set_scale('m'), bvpr[k].set_scale('m')
    time_plot(ecv.asd_static_3d,bvtg, bvpr, show=False, filename=POUTS["png"], title="ASD (m)")
    show_res("image", POUTS["png"])
    print("Let's take it up a notch and have an interactive 3D plot!")
    time_plot(ecv.interactive_3d, bvinp, bvtg, show=False, filename=POUTS["html"],
              title="Input & labels")
    show_res("web file", POUTS["html"])
    #SDF (mm)
    bvinp.set_scale("mm")
    for k in bvtg.keys():
        bvtg[k].set_scale("mm"), bvpr[k].set_scale("mm")
    time_plot(ecv.sdf_interactive_3d, bvtg, bvpr, vinputs=bvinp, title="SDF (mm)")
    # ASD (m)
    bvinp.set_scale('m')
    for k in bvtg.keys():
        bvtg[k].set_scale('m'), bvpr[k].set_scale('m')
    time_plot(ecv.asd_interactive_3d, bvtg, bvpr, title="ASD (m)", show=False, filename=POUTS["html"])
    show_res("web file", POUTS["html"])
    print("Back to 2D! But with a twist... It's animated o/")
    time_plot(ecv.sliced_volume, bvinp, bvtg, axis=2, vpreds=bvpr, stride=5,
              plot_input=False, filename=POUTS["gif"], title="Labels on input & predictions")
    show_res("gif", POUTS["gif"])
    if not isinstance(vinp, list):
        the_end("You didn't give a sequence, so I can't further unfortunately. Hope you still had fun!")
        return
    time_plot(ecv.sliced_sequence, vinp, vtg, 64, axis=0, filename=POUTS["gif"], title="Input & labels")
    show_res("gif", POUTS["gif"])
    print("And for the grand finale... Interactive 3D animated plot!!")
    time_plot(ecv.animated_3d, vinp, None, vpreds=vpr,
              filename=POUTS["html"], title="Input & predictions", show=False)
    show_res("web file", POUTS["html"])
    #SDF (m)
    time_plot(ecv.sdf_animated_3d, vtg, vpr, vinputs=vinp, title="SDF (m)", show=False, filename=POUTS["html"])
    show_res("web file", POUTS["html"])
    # ASD (mm)
    for i in range(len(vinp)):
        vinp[i].set_scale("mm")
    for k in vtg.keys():
        for i in range(len(vtg[k])):
            vtg[k][i].set_scale("mm"), vpr[k][i].set_scale("mm")
    time_plot(ecv.asd_animated_3d, vtg, vpr, title="ASD (mm)", show=True)
    the_end("That's all folks!")


if __name__ == "__main__":
    testy_testa()
