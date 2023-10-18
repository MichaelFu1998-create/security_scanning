def grid_1d(self):
        """ The arc second-grid of (y,x) coordinates of every pixel.

        This is defined from the top-left corner, such that the first pixel at location [0, 0] will have a negative x \
        value y value in arc seconds.
        """
        return grid_util.regular_grid_1d_from_shape_pixel_scales_and_origin(shape=self.shape,
                                                                            pixel_scales=self.pixel_scales,
                                                                            origin=self.origin)