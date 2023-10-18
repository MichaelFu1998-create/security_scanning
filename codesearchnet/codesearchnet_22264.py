def sigma(self):
        """
        Spot size of matched beam :math:`\\left( \\frac{2 E \\varepsilon_0 }{ n_p e^2 } \\right)^{1/4} \\sqrt{\\epsilon}`
        """
        return _np.power(2*_sltr.GeV2joule(self.E)*_spc.epsilon_0 / (self.plasma.n_p * _np.power(_spc.elementary_charge, 2)) , 0.25) * _np.sqrt(self.emit)