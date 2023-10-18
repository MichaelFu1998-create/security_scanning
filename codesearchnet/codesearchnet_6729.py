def k(self):
        r'''Thermal conductivity of the chemical at its current phase,
        temperature, and pressure in units of [W/m/K].

        Utilizes the object oriented interfaces
        :obj:`thermo.thermal_conductivity.ThermalConductivityLiquid` and
        :obj:`thermo.thermal_conductivity.ThermalConductivityGas` to perform
        the actual calculation of each property.

        Examples
        --------
        >>> Chemical('ethanol', T=300).kl
        0.16313594741877802
        >>> Chemical('ethanol', T=400).kg
        0.026019924109310026
        '''
        return phase_select_property(phase=self.phase, s=None, l=self.kl, g=self.kg)