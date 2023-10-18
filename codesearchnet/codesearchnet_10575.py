def padded_grid_from_mask_sub_grid_size_and_psf_shape(cls, mask, sub_grid_size, psf_shape):
        """Setup an *PaddedSubGrid* for an input mask, sub-grid size and psf-shape.

        The center of every sub-pixel is used to setup the grid's (y,x) arc-second coordinates, including \
        masked-pixels which are beyond the input shape but will have light blurred into them given the psf-shape.

        Parameters
        ----------
        mask : Mask
            The mask whose masked pixels are used to setup the sub-pixel grid_stack.
        sub_grid_size : int
            The size (sub_grid_size x sub_grid_size) of each image-pixels sub-grid.
        psf_shape : (int, int)
           The shape of the psf which defines the blurring region and therefore size of padding.
        """

        padded_shape = (mask.shape[0] + psf_shape[0] - 1, mask.shape[1] + psf_shape[1] - 1)

        padded_sub_grid = grid_util.sub_grid_1d_masked_from_mask_pixel_scales_and_sub_grid_size(
            mask=np.full(padded_shape, False), pixel_scales=mask.pixel_scales, sub_grid_size=sub_grid_size)

        padded_mask = msk.Mask.unmasked_for_shape_and_pixel_scale(shape=padded_shape, pixel_scale=mask.pixel_scale)

        return PaddedSubGrid(arr=padded_sub_grid, mask=padded_mask, image_shape=mask.shape,
                             sub_grid_size=sub_grid_size)