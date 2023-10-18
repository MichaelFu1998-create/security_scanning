def intensities_from_grid(self, grid):
        """Calculate the summed intensities of all of the galaxy's light profiles using a grid of Cartesian (y,x) \
        coordinates.
        
        If the galaxy has no light profiles, a grid of zeros is returned.
        
        See *profiles.light_profiles* for a description of how light profile intensities are computed.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        """
        if self.has_light_profile:
            return sum(map(lambda p: p.intensities_from_grid(grid), self.light_profiles))
        else:
            return np.zeros((grid.shape[0],))