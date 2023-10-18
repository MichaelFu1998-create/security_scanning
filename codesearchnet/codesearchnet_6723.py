def rho(self):
        r'''Mass density of the chemical at its current phase and
        temperature and pressure, in units of [kg/m^3].

        Utilizes the object oriented interfaces
        :obj:`thermo.volume.VolumeSolid`,
        :obj:`thermo.volume.VolumeLiquid`,
        and :obj:`thermo.volume.VolumeGas` to perform the
        actual calculation of each property. Note that those interfaces provide
        output in units of m^3/mol.

        Examples
        --------
        >>> Chemical('decane', T=550, P=2E6).rho
        498.67008448640604
        '''
        return phase_select_property(phase=self.phase, s=self.rhos, l=self.rhol, g=self.rhog)