def from_shape_and_pixel_scale(cls, shape, pixel_scale):
        """Setup a regular-grid from a 2D array shape and pixel scale. Here, the center of every pixel on the 2D \
        array gives the grid's (y,x) arc-second coordinates. 
         
        This is equivalent to using a 2D mask consisting entirely of unmasked pixels.

        Parameters
        -----------
        shape : (int, int)
            The 2D shape of the array, where all pixels are used to generate the grid-stack's grid_stack.
        pixel_scale : float
            The size of each pixel in arc seconds.                 
        """
        mask = msk.Mask.unmasked_for_shape_and_pixel_scale(shape=shape, pixel_scale=pixel_scale)
        array = grid_util.regular_grid_1d_masked_from_mask_pixel_scales_and_origin(mask=mask,
                                                                                   pixel_scales=mask.pixel_scales)
        return cls(array, mask)