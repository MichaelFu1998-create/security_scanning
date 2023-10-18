def rhos(self):
        r'''Solid-phase mass density of the chemical at its current temperature,
        in units of [kg/m^3]. For calculation of this property at
        other temperatures, or specifying manually the method used
        to calculate it, and more - see the object oriented interface
        :obj:`thermo.volume.VolumeSolid`; each Chemical instance
        creates one to actually perform the calculations. Note that that
        interface provides output in molar units.

        Examples
        --------
        >>> Chemical('iron').rhos
        7869.999999999994
        '''
        Vms = self.Vms
        if Vms:
            return Vm_to_rho(Vms, self.MW)
        return None