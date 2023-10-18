def estimated_noise_map_counts(self):
        """ The estimated noise_maps mappers of the image (using its background noise_maps mappers and image values
        in counts) in counts.
        """
        return np.sqrt((np.abs(self.image_counts) + np.square(self.background_noise_map_counts)))