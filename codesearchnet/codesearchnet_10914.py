def diffusion_coeff_counts(self):
        """List of tuples of (diffusion coefficient, counts) pairs.

        The order of the diffusion coefficients is as in self.diffusion_coeff.
        """
        return [(key, len(list(group)))
                for key, group in itertools.groupby(self.diffusion_coeff)]