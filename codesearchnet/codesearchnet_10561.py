def from_mask_and_sub_grid_size(cls, mask, sub_grid_size=1):
        """Setup a sub-grid of the unmasked pixels, using a mask and a specified sub-grid size. The center of \
        every unmasked pixel's sub-pixels give the grid's (y,x) arc-second coordinates.

        Parameters
        -----------
        mask : Mask
            The mask whose masked pixels are used to setup the sub-pixel grid_stack.
        sub_grid_size : int
            The size (sub_grid_size x sub_grid_size) of each unmasked pixels sub-grid.
        """
        sub_grid_masked = grid_util.sub_grid_1d_masked_from_mask_pixel_scales_and_sub_grid_size(
            mask=mask,
            pixel_scales=mask.pixel_scales,
            sub_grid_size=sub_grid_size)
        return SubGrid(sub_grid_masked, mask, sub_grid_size)