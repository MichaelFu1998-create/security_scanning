def grid_arcsec_to_grid_pixel_centres(self, grid_arcsec):
        """Convert a grid of (y,x) arc second coordinates to a grid of (y,x) pixel values. Pixel coordinates are \
        returned as integers such that they map directly to the pixel they are contained within.

        The pixel coordinate origin is at the top left corner of the grid, such that the pixel [0,0] corresponds to \
        higher y arc-second coordinate value and lowest x arc-second coordinate.

        The arc-second coordinate origin is defined by the class attribute origin, and coordinates are shifted to this \
        origin before computing their 1D grid pixel indexes.

        Parameters
        ----------
        grid_arcsec: ndarray
            The grid of (y,x) coordinates in arc seconds.
        """
        return grid_util.grid_arcsec_1d_to_grid_pixel_centres_1d(grid_arcsec_1d=grid_arcsec,
                                                                      shape=self.shape,
                                                                      pixel_scales=self.pixel_scales,
                                                                      origin=self.origin).astype('int')