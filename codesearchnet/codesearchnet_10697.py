def grid_pixels_to_grid_arcsec(self, grid_pixels):
        """Convert a grid of (y,x) pixel coordinates to a grid of (y,x) arc second values.

        The pixel coordinate origin is at the top left corner of the grid, such that the pixel [0,0] corresponds to \
        higher y arc-second coordinate value and lowest x arc-second coordinate.

        The arc-second coordinate origin is defined by the class attribute origin, and coordinates are shifted to this \
        origin before computing their 1D grid pixel indexes.

        Parameters
        ----------
        grid_pixels : ndarray
            The grid of (y,x) coordinates in pixels.
        """
        return grid_util.grid_pixels_1d_to_grid_arcsec_1d(grid_pixels_1d=grid_pixels, shape=self.shape,
                                                               pixel_scales=self.pixel_scales, origin=self.origin)