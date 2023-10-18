def Vm(self):
        r'''Molar volume of the chemical at its current phase and
        temperature and pressure, in units of [m^3/mol].

        Utilizes the object oriented interfaces
        :obj:`thermo.volume.VolumeSolid`,
        :obj:`thermo.volume.VolumeLiquid`,
        and :obj:`thermo.volume.VolumeGas` to perform the
        actual calculation of each property.

        Examples
        --------
        >>> Chemical('ethylbenzene', T=550, P=3E6).Vm
        0.00017758024401627633
        '''
        return phase_select_property(phase=self.phase, s=self.Vms, l=self.Vml, g=self.Vmg)