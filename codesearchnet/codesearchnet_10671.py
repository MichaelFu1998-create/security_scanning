def grid_to_elliptical_radii(self, grid):
        """ Convert a grid of (y,x) coordinates to an elliptical radius.

        If the coordinates have not been transformed to the profile's geometry, this is performed automatically.

        Parameters
        ----------
        grid : TransformedGrid(ndarray)
            The (y, x) coordinates in the reference frame of the elliptical profile.
        """
        return np.sqrt(np.add(np.square(grid[:, 1]), np.square(np.divide(grid[:, 0], self.axis_ratio))))