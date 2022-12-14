import numpy as np
import plotly.graph_objects as go

from skimage.measure import marching_cubes



class VoxelGrid:
    # Code originating from Sverre Herland
    """ Wrapper for voxel grid and its relevant information for plotting """
    def __init__(self, grid, origin, directions, spacing):
        """
        grid:
        """
        grid = grid if isinstance(grid, np.ndarray) else np.array(grid)
        origin = origin if isinstance(origin, np.ndarray) else np.array(origin)
        directions = directions if isinstance(directions, np.ndarray) else np.array(directions)
        spacing = spacing if isinstance(spacing, np.ndarray) else np.array(spacing)
        assert grid.ndim == 3
        assert origin.shape == (3,)
        assert directions.shape == (3, 3)
        assert spacing.shape == (3,)
        self.values = grid
        self.origin = origin
        self.directions = directions
        self.spacing = spacing
        #FIXME: ALlow to add devoxelize parameters as attributes

    @classmethod
    def fromh5(cls, filename):
        #TODO? Allow from open file too
        pass #TODO

    @classmethod
    def fromply(cls, filename, origin, directions, spacing):
        pass #TODO


    @property
    def shape(self):
        return self.values.shape

    def devoxelize(self, level=None, mask=False, stride=1):
        # Use for 3D plotting
        verts, faces, _, values = marching_cubes(self.values, level,
                                                 spacing=1 / np.array(self.shape),
                                                 step_size=stride, allow_degenerate=False,
                                                 mask=self.values > 0 if mask else None)
        # Map to coordinates given by voxel grid. Need right multiplication
        verts = verts @ self.directions + self.origin
        return verts, faces, values

    def make_mesh(self, level=None, mask=False, stride=1, **kwargs):
        # Create Plotly 3D mesh
        verts, faces, values = self.devoxelize(level, mask, stride)
        x, y, z = zip(*verts)
        i, j, k = zip(*faces)
        intensity = None if "color" in kwargs else values
        return go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, intensity=intensity, **kwargs)

    def float2bool(self, threshold=0.5, key=None):
        # Use for slice plotting
        #FIXME: Handle multiclass
        mask = (self.values[key] if key else self.values) > threshold
        return VoxelGrid(np.where(mask, 1, 0).astype(np.uint8), self.origin,
                         self.directions, self.spacing)
