def hyper_noise_from_contributions(self, noise_map, contributions):
        """Compute a scaled galaxy hyper noise-map from a baseline noise-map.

        This uses the galaxy contribution map and the *noise_factor* and *noise_power* hyper-parameters.

        Parameters
        -----------
        noise_map : ndarray
            The observed noise-map (before scaling).
        contributions : ndarray
            The galaxy contribution map.
        """
        return self.noise_factor * (noise_map * contributions) ** self.noise_power