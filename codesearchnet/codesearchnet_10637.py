def deflections_from_grid(self, grid):
        """Compute the summed (y,x) deflection angles of the galaxy's mass profiles using a grid of Cartesian (y,x) \
        coordinates.

        If the galaxy has no mass profiles, two grid of zeros are returned.

        See *profiles.mass_profiles* module for details of how this is performed.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        """
        if self.has_mass_profile:
            return sum(map(lambda p: p.deflections_from_grid(grid), self.mass_profiles))
        else:
            return np.full((grid.shape[0], 2), 0.0)