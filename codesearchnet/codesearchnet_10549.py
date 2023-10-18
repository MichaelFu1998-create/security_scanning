def grid_stack_for_simulation(cls, shape, pixel_scale, psf_shape, sub_grid_size=2):
        """Setup a grid-stack of grid_stack for simulating an image of a strong lens, whereby the grid's use \
        padded-grid_stack to ensure that the PSF blurring in the simulation routine (*ccd.PrepatoryImage.simulate*) \
        is not degraded due to edge effects.

        Parameters
        -----------
        shape : (int, int)
            The 2D shape of the array, where all pixels are used to generate the grid-stack's grid_stack.
        pixel_scale : float
            The size of each pixel in arc seconds.            
        psf_shape : (int, int)
            The shape of the PSF used in the analysis, which defines how much the grid's must be masked to mitigate \
            edge effects.
        sub_grid_size : int
            The size of a sub-pixel's sub-grid (sub_grid_size x sub_grid_size).
        """
        return cls.padded_grid_stack_from_mask_sub_grid_size_and_psf_shape(mask=msk.Mask(array=np.full(shape, False),
                                                                                         pixel_scale=pixel_scale),
                                                                           sub_grid_size=sub_grid_size,
                                                                           psf_shape=psf_shape)