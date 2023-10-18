def Zs(self):
        r'''Compressibility factor of the chemical in the solid phase at the
        current temperature and pressure, [dimensionless].

        Utilizes the object oriented interface and
        :obj:`thermo.volume.VolumeSolid` to perform the actual calculation of
        molar volume.

        Examples
        --------
        >>> Chemical('palladium').Z
        0.00036248477437931853
        '''
        Vms = self.Vms
        if Vms:
            return Z(self.T, self.P, Vms)
        return None