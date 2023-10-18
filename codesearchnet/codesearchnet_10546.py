def grid_stack_from_mask_sub_grid_size_and_psf_shape(cls, mask, sub_grid_size, psf_shape):
        """Setup a grid-stack of grid_stack from a mask, sub-grid size and psf-shape.

        Parameters
        -----------
        mask : Mask
            The mask whose unmasked pixels (*False*) are used to generate the grid-stack's grid_stack.
        sub_grid_size : int
            The size of a sub-pixel's sub-grid (sub_grid_size x sub_grid_size).
        psf_shape : (int, int)
            the shape of the PSF used in the analysis, which defines the mask's blurring-region.
        """
        regular_grid = RegularGrid.from_mask(mask)
        sub_grid = SubGrid.from_mask_and_sub_grid_size(mask, sub_grid_size)
        blurring_grid = RegularGrid.blurring_grid_from_mask_and_psf_shape(mask, psf_shape)
        return GridStack(regular_grid, sub_grid, blurring_grid)