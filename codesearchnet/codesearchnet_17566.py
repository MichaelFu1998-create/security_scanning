def h_x(self, L, theta, Ts, **statef):
        """
        Calculate the local heat transfer coefficient.

        :param L: [m] characteristic length of the heat transfer surface
        :param theta: [°] angle of the surface with the vertical
        :param Ts: [K] heat transfer surface temperature
        :param Tf: [K] bulk fluid temperature

        :returns: [W/m2/K] float
        """

        Nu_x = self.Nu_x(L, theta, Ts, **statef)
        k = self._fluid.k(T=self.Tr)
        return Nu_x * k / L