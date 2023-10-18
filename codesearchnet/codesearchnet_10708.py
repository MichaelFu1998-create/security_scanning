def unmasked_for_shape_and_pixel_scale(cls, shape, pixel_scale, invert=False):
        """Setup a mask where all pixels are unmasked.

        Parameters
        ----------
        shape : (int, int)
            The (y,x) shape of the mask in units of pixels.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        """
        mask = np.full(tuple(map(lambda d: int(d), shape)), False)
        if invert: mask = np.invert(mask)
        return cls(array=mask, pixel_scale=pixel_scale)