def lambda_large(self, r0):
        """
        The wavelength for large (:math:`r_0 < \\sigma_r`) oscillations.
        """
        return 2*_np.sqrt(2*_np.pi/self.k)*r0