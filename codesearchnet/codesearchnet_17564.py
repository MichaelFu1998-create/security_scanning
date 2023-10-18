def Nu_x(self, L, theta, Ts, **statef):
        """
        Calculate the local Nusselt number.

        :param L: [m] characteristic length of the heat transfer surface
        :param theta: [°] angle of the surface with the vertical
        :param Ts: [K] heat transfer surface temperature
        :param Tf: [K] bulk fluid temperature

        :returns: float
        """

        Tf = statef['T']
        thetar = radians(theta)

        if self._isgas:
            self.Tr = Ts - 0.38 * (Ts - Tf)
            beta = self._fluid.beta(T=Tf)
        else:  # for liquids
            self.Tr = Ts - 0.5 * (Ts - Tf)
            beta = self._fluid.beta(T=self.Tr)

        if Ts > Tf:  # hot surface
            if 0.0 < theta < 45.0:
                g = const.g*cos(thetar)
            else:
                g = const.g
        else:  # cold surface
            if -45.0 < theta < 0.0:
                g = const.g*cos(thetar)
            else:
                g = const.g

        nu = self._fluid.nu(T=self.Tr)
        alpha = self._fluid.alpha(T=self.Tr)

        Gr = dq.Gr(L, Ts, Tf, beta, nu, g)
        Pr = dq.Pr(nu, alpha)
        Ra = Gr * Pr

        eq = [self.equation_dict[r]
              for r in self.regions if r.contains_point(theta, Ra)][0]

        return eq(self, Ra, Pr)