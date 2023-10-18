def Zl_STP(self):
        r'''Liquid-phase compressibility factor of the mixture at 298.15 K and 101.325 kPa,
        and the current composition, [dimensionless].

        Examples
        --------
        >>> Mixture(['cyclobutane'], ws=[1]).Zl_STP
        0.0033285083663950068
        '''
        Vml = self.Vml
        if Vml:
            return Z(self.T, self.P, Vml)
        return None