def r_small(self, x, r0):
        """
        Approximate trajectory function for small (:math:`r_0 < \\sigma_r`) oscillations.
        """
        return r0*_np.cos(_np.sqrt(self.k_small) * x)