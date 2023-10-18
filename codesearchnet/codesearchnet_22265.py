def sigma_prime(self):
        """
        Divergence of matched beam
        """
        return _np.sqrt(self.emit/self.beta(self.E))