def grid_to_eccentric_radii(self, grid):
        """Convert a grid of (y,x) coordinates to an eccentric radius, which is (1.0/axis_ratio) * elliptical radius \
        and used to define light profile half-light radii using circular radii.

        If the coordinates have not been transformed to the profile's geometry, this is performed automatically.

        Parameters
        ----------
        grid : TransformedGrid(ndarray)
            The (y, x) coordinates in the reference frame of the elliptical profile.
        """
        return np.multiply(np.sqrt(self.axis_ratio), self.grid_to_elliptical_radii(grid)).view(np.ndarray)