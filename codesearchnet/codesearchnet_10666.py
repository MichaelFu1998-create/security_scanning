def transform_grid_to_reference_frame(self, grid):
        """Transform a grid of (y,x) coordinates to the reference frame of the profile, including a translation to \
        its centre.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        """
        transformed = np.subtract(grid, self.centre)
        return transformed.view(TransformedGrid)