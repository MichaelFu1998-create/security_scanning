def _kurtosis(self, x, z, d=0):
        """ returns the kurtosis parameter for direction d, d=0 is rho, d=1 is z """
        val = self._poly(z, self._kurtosis_coeffs(d))
        return (np.tanh(val)+1)/12.*(3 - 6*x**2 + x**4)