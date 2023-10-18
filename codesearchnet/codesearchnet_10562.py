def from_shape_pixel_scale_and_sub_grid_size(cls, shape, pixel_scale, sub_grid_size):
        """Setup a sub-grid from a 2D array shape and pixel scale. Here, the center of every pixel on the 2D \
        array gives the grid's (y,x) arc-second coordinates, where each pixel has sub-pixels specified by the \
        sub-grid size.

        This is equivalent to using a 2D mask consisting entirely of unmasked pixels.

        Parameters
        -----------
        shape : (int, int)
            The 2D shape of the array, where all pixels are used to generate the grid-stack's grid_stack.
        pixel_scale : float
            The size of each pixel in arc seconds.
        sub_grid_size : int
            The size (sub_grid_size x sub_grid_size) of each unmasked pixels sub-grid.
        """
        mask = msk.Mask.unmasked_for_shape_and_pixel_scale(shape=shape, pixel_scale=pixel_scale)
        sub_grid = grid_util.sub_grid_1d_masked_from_mask_pixel_scales_and_sub_grid_size(mask=mask,
                                                                                         pixel_scales=mask.pixel_scales,
                                                                                         sub_grid_size=sub_grid_size)
        return SubGrid(sub_grid, mask, sub_grid_size)