def simulate_variable_arrays(cls, array, pixel_scale, exposure_time_map, psf=None, background_sky_map=None,
                                 add_noise=True, noise_if_add_noise_false=0.1, noise_seed=-1, name=None):
        """
        Create a realistic simulated image by applying effects to a plain simulated image.

        Parameters
        ----------
        name
        array : ndarray
            The image before simulating (e.g. the lens and source galaxies before optics blurring and CCD read-out).
        pixel_scale: float
            The scale of each pixel in arc seconds
        exposure_time_map : ndarray
            An array representing the effective exposure time of each pixel.
        psf: PSF
            An array describing the PSF the simulated image is blurred with.
        background_sky_map : ndarray
            The value of background sky in every image pixel (electrons per second).
        add_noise: Bool
            If True poisson noise_maps is simulated and added to the image, based on the total counts in each image
            pixel
        noise_seed: int
            A seed for random noise_maps generation
        """

        if background_sky_map is not None:
            array += background_sky_map

        if psf is not None:
            array = psf.convolve(array)
            array = cls.trim_psf_edges(array, psf)
            exposure_time_map = cls.trim_psf_edges(exposure_time_map, psf)
            if background_sky_map is not None:
                background_sky_map = cls.trim_psf_edges(background_sky_map, psf)

        if add_noise is True:
            array += generate_poisson_noise(array, exposure_time_map, noise_seed)
            array_counts = np.multiply(array, exposure_time_map)
            noise_map = np.divide(np.sqrt(array_counts), exposure_time_map)
        else:
            noise_map = noise_if_add_noise_false * np.ones(array.shape)

        if np.isnan(noise_map).any():
            raise exc.DataException('The noise-map has NaN values in it. This suggests your exposure time and / or'
                                       'background sky levels are too low, create signal counts at or close to 0.0.')

        if background_sky_map is not None:
            array -= background_sky_map

        # ESTIMATE THE BACKGROUND NOISE MAP FROM THE IMAGE

        if background_sky_map is not None:
            background_noise_map_counts = np.sqrt(np.multiply(background_sky_map, exposure_time_map))
            background_noise_map = np.divide(background_noise_map_counts, exposure_time_map)
        else:
            background_noise_map = None

        # ESTIMATE THE POISSON NOISE MAP FROM THE IMAGE

        array_counts = np.multiply(array, exposure_time_map)
        poisson_noise_map = np.divide(np.sqrt(np.abs(array_counts)), exposure_time_map)

        array = ScaledSquarePixelArray(array=array, pixel_scale=pixel_scale)
        noise_map = NoiseMap(array=noise_map, pixel_scale=pixel_scale)

        if background_noise_map is not None:
            background_noise_map = NoiseMap(array=background_noise_map, pixel_scale=pixel_scale)

        if poisson_noise_map is not None:
            poisson_noise_map = PoissonNoiseMap(array=poisson_noise_map, pixel_scale=pixel_scale)

        return CCDData(array, pixel_scale=pixel_scale, psf=psf, noise_map=noise_map,
                       background_noise_map=background_noise_map, poisson_noise_map=poisson_noise_map,
                       exposure_time_map=exposure_time_map, background_sky_map=background_sky_map, name=name)