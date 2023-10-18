def absolute_signal_to_noise_map(self):
        """The estimated absolute_signal-to-noise_maps mappers of the image."""
        return np.divide(np.abs(self.image), self.noise_map)