def h_L(self, L, theta, Ts, **statef):
        """
        Calculate the average heat transfer coefficient.

        :param L: [m] characteristic length of the heat transfer surface
        :param theta: [°] angle of the surface with the vertical
        :param Ts: [K] heat transfer surface temperature
        :param Tf: [K] bulk fluid temperature

        :returns: [W/m2/K] float
        """

        Nu_L = self.Nu_L(L, theta, Ts, **statef)
        k = self._fluid.k(T=self.Tr)
        return Nu_L * k / L