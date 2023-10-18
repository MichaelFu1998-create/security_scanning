def from_weight_map(cls, pixel_scale, weight_map):
        """Setup the noise-map from a weight map, which is a form of noise-map that comes via HST image-reduction and \
        the software package MultiDrizzle.

        The variance in each pixel is computed as:

        Variance = 1.0 / sqrt(weight_map).

        The weight map may contain zeros, in which cause the variances are converted to large values to omit them from \
        the analysis.

        Parameters
        -----------
        pixel_scale : float
            The size of each pixel in arc seconds.
        weight_map : ndarray
            The weight-value of each pixel which is converted to a variance.
        """
        np.seterr(divide='ignore')
        noise_map = 1.0 / np.sqrt(weight_map)
        noise_map[noise_map == np.inf] = 1.0e8
        return NoiseMap(array=noise_map, pixel_scale=pixel_scale)