def _construct_coefficients(self):
        """Calculate the coefficients based on the func, degree, and
        interpolating points.
        _coeffs is a [order, N,M,....] array

        Notes
        -----
        Moved the -c0 to the coefficients defintion
        app -= 0.5 * self._coeffs[0] -- moving this to the coefficients
        """
        coeffs = [0]*self.degree

        N = float(self.evalpts)

        lvals = np.arange(self.evalpts).astype('float')
        xpts = self._c2x(np.cos(np.pi*(lvals + 0.5)/N))
        fpts = np.rollaxis(self.func(xpts, *self.args), -1)

        for a in range(self.degree):
            inner = [
                fpts[b] * np.cos(np.pi*a*(lvals[b]+0.5)/N)
                for b in range(self.evalpts)
            ]
            coeffs[a] = 2.0/N * np.sum(inner, axis=0)

        coeffs[0] *= 0.5
        self._coeffs = np.array(coeffs)