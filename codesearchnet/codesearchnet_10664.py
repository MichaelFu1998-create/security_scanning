def grid_to_grid_radii(self, grid):
        """Convert a grid of (y, x) coordinates to a grid of their circular radii.

        If the coordinates have not been transformed to the profile's centre, this is performed automatically.

        Parameters
        ----------
        grid : TransformedGrid(ndarray)
            The (y, x) coordinates in the reference frame of the profile.
        """
        return np.sqrt(np.add(np.square(grid[:, 0]), np.square(grid[:, 1])))