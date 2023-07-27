from pathlib import Path



def clean_fname(fname, ext=".html"):
    fname = Path(fname).resolve().expanduser()
    if fname.suffix != ext:
        fname = fname.with_suffix(ext)
    return fname
