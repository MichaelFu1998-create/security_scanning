def elliptical_annular(cls, shape, pixel_scale,inner_major_axis_radius_arcsec, inner_axis_ratio, inner_phi,
                           outer_major_axis_radius_arcsec, outer_axis_ratio, outer_phi, centre=(0.0, 0.0),
                           invert=False):
        """Setup a mask where unmasked pixels are within an elliptical annulus of input inner and outer arc second \
        major-axis and centre.

        Parameters
        ----------
        shape: (int, int)
            The (y,x) shape of the mask in units of pixels.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        inner_major_axis_radius_arcsec : float
            The major-axis (in arc seconds) of the inner ellipse within which pixels are masked.
        inner_axis_ratio : float
            The axis-ratio of the inner ellipse within which pixels are masked.
        inner_phi : float
            The rotation angle of the inner ellipse within which pixels are masked, (counter-clockwise from the \
            positive x-axis).
        outer_major_axis_radius_arcsec : float
            The major-axis (in arc seconds) of the outer ellipse within which pixels are unmasked.
        outer_axis_ratio : float
            The axis-ratio of the outer ellipse within which pixels are unmasked.
        outer_phi : float
            The rotation angle of the outer ellipse within which pixels are unmasked, (counter-clockwise from the \
            positive x-axis).
        centre: (float, float)
            The centre of the elliptical annuli used to mask pixels.
        """
        mask = mask_util.mask_elliptical_annular_from_shape_pixel_scale_and_radius(shape, pixel_scale,
                           inner_major_axis_radius_arcsec, inner_axis_ratio, inner_phi,
                           outer_major_axis_radius_arcsec, outer_axis_ratio, outer_phi, centre)
        if invert: mask = np.invert(mask)
        return cls(array=mask.astype('bool'), pixel_scale=pixel_scale)