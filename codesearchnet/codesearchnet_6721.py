def Cpm(self):
        r'''Molar heat capacity of the chemical at its current phase and
        temperature, in units of [J/mol/K].

        Utilizes the object oriented interfaces
        :obj:`thermo.heat_capacity.HeatCapacitySolid`,
        :obj:`thermo.heat_capacity.HeatCapacityLiquid`,
        and :obj:`thermo.heat_capacity.HeatCapacityGas` to perform the
        actual calculation of each property.

        Examples
        --------
        >>> Chemical('cubane').Cpm
        137.05489206785944
        >>> Chemical('ethylbenzene', T=550, P=3E6).Cpm
        294.18449553310046
        '''
        return phase_select_property(phase=self.phase, s=self.Cpsm, l=self.Cplm, g=self.Cpgm)