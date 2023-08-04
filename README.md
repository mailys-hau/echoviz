<div align="center">
<h1>EchoViz</h1>

[![Stable](https://img.shields.io/badge/docs-soon-blue.svg)](https://blank.page/)
[![PyPI Latest Release](https://img.shields.io/pypi/v/echoviz-MALOU.svg)](https://pypi.org/project/echoviz-MALOU/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg?logo=python.svg)](https://www.python.org/)
[![Plotly Version](https://img.shields.io/badge/plotly-v5.15.0-blue.svg?logo=plotly.svg)](https://plotly.com/python/)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/mailys-hau/echoviz/blob/main/LICENSE)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

</div>

Visualization of (3D) echocardiograms in various ways using `plotly`. This does not include pre-processing of the data from DICOMs to the voxel grid.


## Installation

Run `$ pip install echoviz-malou`. This will automatically install needed dependencies.

## Features (= Documentation attempt)

`echoviz` allows you to view 3D voxel grids in different ways:
- 2D slice of the grid
  - `plot_slice`       2D slice of a voxel grid along chosen axis and slice, saved as PNG
  - `sliced_sequence`  2D slice of several voxel grids along the same chosen axis and slice, saved as GIF
  - `sliced_volume`    2D slices of one voxel grid along chosen axis for all slices (you can specify a stride), saved as GIF
- 3D (interactive plot or "static", i.e. screenshot of the interactive view)
  - `interactive_3d`  3D view of a voxel grid that the user can rotate and zoom in, saved as HTML
  - `static_3d`       Screenshot of above function output
- 4D for a sequence of voxel grids
  - `animated_3d`  3D view of several voxel grids that the user can rotate and zoom in, saved as HTML
It is possible to add a target and/or a prediction on top of the input plot. In 2D they will be plotted side by side, in 3D they'll be plotted on top of each other.

In 3D it is also possible to plot the Signed Distance Function as a heatmap between the target and the prediction (negative when the prediction is inside the target). "ASD" is also available, it's the absolute value of the SDF.
- `sdf_[interactive|static|animated]_3d`
- `asd_[interactive|static|animated]_3d`

All functions expect to receive inputs as `VoxelGrid` or a list of `VoxelGrid`. Annotations/labels and predictions are **dictionaries** containing a `VoxelGrid` or list of `VoxelGrid` per key (keys are used to get the plot colour, chose between "all", "anterior" or "posterior".

## Examples

See `tests/test.py` and `tests/test.ipynb`.

 NB: Some additional packages are needed to run the test scripts,
 - For `tests/test.py`, run `$ pip install h5py click`
 - For `tests/test.ipynb` run `$ pip install jupyterlab ipywidgets jupyter-dash`

## Troubleshooting

### Kaleido permission denied
You may need to make Kaleido executable files as executable manually: `chmod +x ~/<venv_name>/lib/python3.9/site-packages/kaleido-<version_number>.egg/kaleido/executable/kaleido ~/<venv_name>/lib/python3.9/site-packages/kaleido-<version_number>.egg/kaleido/executable/bin/kaleido`
For more detail see [here](https://stackoverflow.com/questions/43329028/ioerror-errno-13-permission-denied-when-trying-to-import-and-use-plotly)

### Other
Please report any issues via the GitHub [issues tracker](https://github.com/mailys-hau/echoviz/issues).

<br>

This package was built to plot TEE images and has not been tested on anything else, if you want to participate, you are more than welcome!
