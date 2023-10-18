def Z(self):
        r'''Compressibility factor of the chemical at its current phase and
        temperature and pressure, [dimensionless].

        Examples
        --------
        >>> Chemical('MTBE', T=900, P=1E-2).Z
        0.9999999999079768
        '''
        Vm = self.Vm
        if Vm:
            return Z(self.T, self.P, Vm)
        return None