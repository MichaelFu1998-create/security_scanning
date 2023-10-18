def Nu_L(self, L, theta, Ts, **statef):
        """
        Calculate the average Nusselt number.

        :param L: [m] characteristic length of the heat transfer surface
        :param theta: [°] angle of the surface with the vertical
        :param Ts: [K] heat transfer surface temperature
        :param **statef: [K] bulk fluid temperature

        :returns: float
        """

        return self.Nu_x(L, theta, Ts, **statef) / 0.75