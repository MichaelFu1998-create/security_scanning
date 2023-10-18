def q(self, x, q0):
        """
        Numerically solved trajectory function for initial conditons :math:`q(0) = q_0` and :math:`q'(0) = 0`.
        """
        y1_0 = q0
        y0_0 = 0
        y0   = [y0_0, y1_0]

        y = _sp.integrate.odeint(self._func, y0, x, Dfun=self._gradient, rtol=self.rtol, atol=self.atol)

        return y[:, 1]