def from_inverse_noise_map(cls, pixel_scale, inverse_noise_map):
        """Setup the noise-map from an root-mean square standard deviation map, which is a form of noise-map that \
        comes via HST image-reduction and the software package MultiDrizzle.

        The variance in each pixel is computed as:

        Variance = 1.0 / inverse_std_map.

        The weight map may contain zeros, in which cause the variances are converted to large values to omit them from \
        the analysis.

        Parameters
        -----------
        pixel_scale : float
            The size of each pixel in arc seconds.
        inverse_noise_map : ndarray
            The inverse noise_map value of each pixel which is converted to a variance.
        """
        noise_map = 1.0 / inverse_noise_map
        return NoiseMap(array=noise_map, pixel_scale=pixel_scale)