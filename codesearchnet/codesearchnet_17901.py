def _skew(self, x, z, d=0):
        """ returns the kurtosis parameter for direction d, d=0 is rho, d=1 is z """
        # get the top bound determined by the kurtosis
        kval = (np.tanh(self._poly(z, self._kurtosis_coeffs(d)))+1)/12.
        bdpoly = np.array([
            -1.142468e+04,  3.0939485e+03, -2.0283568e+02,
            -2.1047846e+01, 3.79808487e+00, 1.19679781e-02
        ])
        top = np.polyval(bdpoly, kval)

        # limit the skewval to be 0 -> top val
        skew = self._poly(z, self._skew_coeffs(d))
        skewval = top*(np.tanh(skew) + 1) - top

        return skewval*(3*x - x**3)