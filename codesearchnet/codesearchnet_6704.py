def Zg(self):
        r'''Compressibility factor of the chemical in the gas phase at the
        current temperature and pressure, [dimensionless].

        Utilizes the object oriented interface and
        :obj:`thermo.volume.VolumeGas` to perform the actual calculation of
        molar volume.

        Examples
        --------
        >>> Chemical('sulfur hexafluoride', T=700, P=1E9).Zg
        11.140084184207813
        '''
        Vmg = self.Vmg
        if Vmg:
            return Z(self.T, self.P, Vmg)
        return None