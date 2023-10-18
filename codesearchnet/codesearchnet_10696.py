def grid_arcsec_to_grid_pixel_indexes(self, grid_arcsec):
        """Convert a grid of (y,x) arc second coordinates to a grid of (y,x) pixel 1D indexes. Pixel coordinates are \
        returned as integers such that they are the pixel from the top-left of the 2D grid going rights and then \
        downwards.

        For example:

        The pixel at the top-left, whose 2D index is [0,0], corresponds to 1D index 0.
        The fifth pixel on the top row, whose 2D index is [0,5], corresponds to 1D index 4.
        The first pixel on the second row, whose 2D index is [0,1], has 1D index 10 if a row has 10 pixels.

        The arc-second coordinate origin is defined by the class attribute origin, and coordinates are shifted to this \
        origin before computing their 1D grid pixel indexes.

        Parameters
        ----------
        grid_arcsec: ndarray
            The grid of (y,x) coordinates in arc seconds.
        """
        return grid_util.grid_arcsec_1d_to_grid_pixel_indexes_1d(grid_arcsec_1d=grid_arcsec,
                                                                      shape=self.shape,
                                                                      pixel_scales=self.pixel_scales,
                                                                      origin=self.origin).astype('int')