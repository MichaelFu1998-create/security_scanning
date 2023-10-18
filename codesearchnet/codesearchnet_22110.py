def emit_measured(self):
        """
        The beam emittance :math:`\\langle x x' \\rangle`.
        """
        return _np.sqrt(self.spotsq*self.divsq-self.xxp**2)