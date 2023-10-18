def r_large(self, x, r0):
        """
        Approximate trajectory function for large (:math:`r_0 > \\sigma_r`) oscillations.
        """
        return r0*_np.cos(x*self.omega_big(r0))