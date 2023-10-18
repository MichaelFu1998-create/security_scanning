def from_mask(cls, mask):
        """Setup a regular-grid from a mask, wehere the center of every unmasked pixel gives the grid's (y,x) \
        arc-second coordinates.

        Parameters
        -----------
        mask : Mask
            The mask whose unmasked pixels are used to setup the regular-pixel grid.
        """
        array = grid_util.regular_grid_1d_masked_from_mask_pixel_scales_and_origin(mask=mask,
                                                                                   pixel_scales=mask.pixel_scales)
        return cls(array, mask)