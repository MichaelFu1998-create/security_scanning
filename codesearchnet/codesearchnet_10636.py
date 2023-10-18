def convergence_from_grid(self, grid):
        """Compute the summed convergence of the galaxy's mass profiles using a grid of Cartesian (y,x) \
        coordinates.

        If the galaxy has no mass profiles, a grid of zeros is returned.
        
        See *profiles.mass_profiles* module for details of how this is performed.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        """
        if self.has_mass_profile:
            return sum(map(lambda p: p.convergence_from_grid(grid), self.mass_profiles))
        else:
            return np.zeros((grid.shape[0],))