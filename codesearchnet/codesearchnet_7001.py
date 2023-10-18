def Zg_STP(self):
        r'''Gas-phase compressibility factor of the mixture at 298.15 K and 101.325 kPa,
        and the current composition, [dimensionless].

        Examples
        --------
        >>> Mixture(['nitrogen'], ws=[1]).Zg_STP
        0.9995520809691023
        '''
        Vmg = self.Vmg
        if Vmg:
            return Z(self.T, self.P, Vmg)
        return None