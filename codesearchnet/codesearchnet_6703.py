def Zl(self):
        r'''Compressibility factor of the chemical in the liquid phase at the
        current temperature and pressure, [dimensionless].

        Utilizes the object oriented interface and
        :obj:`thermo.volume.VolumeLiquid` to perform the actual calculation of
        molar volume.

        Examples
        --------
        >>> Chemical('water').Zl
        0.0007385375470263454
        '''
        Vml = self.Vml
        if Vml:
            return Z(self.T, self.P, Vml)
        return None