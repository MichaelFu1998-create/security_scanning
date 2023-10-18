def simulate_as_gaussian(cls, shape, pixel_scale, sigma, centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0):
        """Simulate the PSF as an elliptical Gaussian profile."""
        from autolens.model.profiles.light_profiles import EllipticalGaussian
        gaussian = EllipticalGaussian(centre=centre, axis_ratio=axis_ratio, phi=phi, intensity=1.0, sigma=sigma)
        grid_1d = grid_util.regular_grid_1d_masked_from_mask_pixel_scales_and_origin(mask=np.full(shape, False),
                                                                                     pixel_scales=(
                                                                                         pixel_scale, pixel_scale))
        gaussian_1d = gaussian.intensities_from_grid(grid=grid_1d)
        gaussian_2d = mapping_util.map_unmasked_1d_array_to_2d_array_from_array_1d_and_shape(array_1d=gaussian_1d,
                                                                                             shape=shape)
        return PSF(array=gaussian_2d, pixel_scale=pixel_scale, renormalize=True)