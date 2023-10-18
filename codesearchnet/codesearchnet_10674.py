def transform_grid_from_reference_frame(self, grid):
        """Transform a grid of (y,x) coordinates from the reference frame of the profile to the original observer \
        reference frame, including a rotation to its original orientation and a translation from the profile's centre.

        Parameters
        ----------
        grid : TransformedGrid(ndarray)
            The (y, x) coordinates in the reference frame of the profile.
        """
        if self.__class__.__name__.startswith("Spherical"):
            return super().transform_grid_from_reference_frame(grid)

        y = np.add(np.add(np.multiply(grid[:, 1], self.sin_phi), np.multiply(grid[:, 0], self.cos_phi)), self.centre[0])
        x = np.add(np.add(np.multiply(grid[:, 1], self.cos_phi), - np.multiply(grid[:, 0], self.sin_phi)),
                   self.centre[1])
        return np.vstack((y, x)).T