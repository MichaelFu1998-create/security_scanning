def Bvirial(self):
        r'''Second virial coefficient of the gas phase of the chemical at its
        current temperature and pressure, in units of [mol/m^3].

        This property uses the object-oriented interface
        :obj:`thermo.volume.VolumeGas`, converting its result with
        :obj:`thermo.utils.B_from_Z`.

        Examples
        --------
        >>> Chemical('water').Bvirial
        -0.0009596286322838357
        '''
        if self.Vmg:
            return B_from_Z(self.Zg, self.T, self.P)
        return None