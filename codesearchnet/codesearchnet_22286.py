def k(self):
        """
        Driving force term: :math:`r'' = -k \\left( \\frac{1-e^{-r^2/2{\\sigma_r}^2}}{r} \\right)`
        """
        try:
            return self._k
        except AttributeError:
            self._k = e**2 * self.N_e / ( (2*_np.pi)**(5/2) * e0 * self.m * c**2 * self.sig_xi)
            return self._k