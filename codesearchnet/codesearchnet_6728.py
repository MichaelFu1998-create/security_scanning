def mu(self):
        r'''Viscosity of the chemical at its current phase, temperature, and
        pressure in units of [Pa*s].

        Utilizes the object oriented interfaces
        :obj:`thermo.viscosity.ViscosityLiquid` and
        :obj:`thermo.viscosity.ViscosityGas` to perform the
        actual calculation of each property.

        Examples
        --------
        >>> Chemical('ethanol', T=300).mu
        0.001044526538460911
        >>> Chemical('ethanol', T=400).mu
        1.1853097849748217e-05
        '''
        return phase_select_property(phase=self.phase, l=self.mul, g=self.mug)