def padded_grid_stack_from_mask_sub_grid_size_and_psf_shape(cls, mask, sub_grid_size, psf_shape):
        """Setup a grid-stack of masked grid_stack from a mask,  sub-grid size and psf-shape.

        Parameters
        -----------
        mask : Mask
            The mask whose masked pixels the grid-stack are setup using.
        sub_grid_size : int
            The size of a sub-pixels sub-grid (sub_grid_size x sub_grid_size).
        psf_shape : (int, int)
            The shape of the PSF used in the analysis, which defines the mask's blurring-region.
        """
        regular_padded_grid = PaddedRegularGrid.padded_grid_from_shape_psf_shape_and_pixel_scale(
            shape=mask.shape,
            psf_shape=psf_shape,
            pixel_scale=mask.pixel_scale)
        sub_padded_grid = PaddedSubGrid.padded_grid_from_mask_sub_grid_size_and_psf_shape(mask=mask,
                                                                                          sub_grid_size=sub_grid_size,
                                                                                          psf_shape=psf_shape)
        # TODO : The blurring grid is not used when the grid mapper is called, the 0.0 0.0 stops errors inr ayT_racing
        # TODO : implement a more explicit solution
        return GridStack(regular=regular_padded_grid, sub=sub_padded_grid, blurring=np.array([[0.0, 0.0]]))