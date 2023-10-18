def k(self):
        """
        Driving force term: :math:`r'' = -k \\left( \\frac{1-e^{-r^2/2{\\sigma_r}^2}}{r} \\right)`
        """
        try:
            return self._k
        except AttributeError:
            self._k = _np.sqrt(_np.pi/8) * e**2 * self.nb0 * self.sig_y / ( e0 * self.m * c**2)
            return self._k