def k_small(self):
        """
        Small-angle driving force term: :math:`r'' = -k_{small} r`.

        Note: :math:`k_{small} = \\frac{k}{2{\\sigma_r^2}}`
        """
        return self.k * _np.sqrt(2/_np.pi) / self.sig_y