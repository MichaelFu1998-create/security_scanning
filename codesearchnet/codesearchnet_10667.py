def transform_grid_from_reference_frame(self, grid):
        """Transform a grid of (y,x) coordinates from the reference frame of the profile to the original observer \
        reference frame, including a translation from the profile's centre.

        Parameters
        ----------
        grid : TransformedGrid(ndarray)
            The (y, x) coordinates in the reference frame of the profile.
        """
        transformed = np.add(grid, self.centre)
        return transformed.view(TransformedGrid)