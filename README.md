# Echoviz
Visualization of (3D) echocardiograms in various ways using `plotly`. This does not include pre-processing of the data from DICOMs to voxel grid.

## Installation

`$ pip install echoviz-malou` This will automatically install needed dependencies.

## Usage

All functions allow you to plot inputs, with annotations and/or predictions if you want to. You can show and / or save the produced figure **except** `sliced_sequence` and `sliced_volume` which can only save it.

Several functions are available:
- `animated_3d`: Interactive 3D plot for all frames in a sequence, saved as HTML
- `interactive_3d`: Interactive 3D of a voxel grid, saved as HTML
- `plot_slice`: 2D slice of a voxel grid, saved as PNG
- `sliced_sequence`: 2D slice for all frames in a sequence, saved as GIF
- `sliced_volume`: All 2D slices in one voxel grid, saved as GIF
- `static_3d`: Screenshot of the interactive 3D plot in default view, saved as PNG

All functions expect to receive inputs, annotations/labels and predictions as either `VoxelGrid` or list/dictionary of `VoxelGrid`.

## Examples

See `tests/test.py` and `tests/test.ipynb`.

 NB: To run the test script and notebook, you'll need to install the aditional packages: `h5py`, `jupyterlab`, `jupyter-dash`.
