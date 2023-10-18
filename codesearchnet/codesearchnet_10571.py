def padded_grid_from_shape_psf_shape_and_pixel_scale(cls, shape, psf_shape, pixel_scale):
        """Setup a regular padded grid from a 2D array shape, psf-shape and pixel-scale.

        The center of every pixel is used to setup the grid's (y,x) arc-second coordinates, including padded pixels \
        which are beyond the input shape but will blurred light into the 2D array's shape due to the psf.

        Parameters
        ----------
        shape : (int, int)
            The (y,x) shape of the masked-grid's 2D image in units of pixels.
        psf_shape : (int, int)
           The shape of the psf which defines the blurring region and therefore size of padding.
        pixel_scale : float
            The scale of each pixel in arc seconds
        """
        padded_shape = (shape[0] + psf_shape[0] - 1, shape[1] + psf_shape[1] - 1)
        padded_regular_grid = grid_util.regular_grid_1d_masked_from_mask_pixel_scales_and_origin(
            mask=np.full(padded_shape, False), pixel_scales=(pixel_scale, pixel_scale))
        padded_mask = msk.Mask.unmasked_for_shape_and_pixel_scale(shape=padded_shape, pixel_scale=pixel_scale)
        return PaddedRegularGrid(arr=padded_regular_grid, mask=padded_mask, image_shape=shape)