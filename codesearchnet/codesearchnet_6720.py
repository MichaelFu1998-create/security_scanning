def Cp(self):
        r'''Mass heat capacity of the chemical at its current phase and
        temperature, in units of [J/kg/K].

        Utilizes the object oriented interfaces
        :obj:`thermo.heat_capacity.HeatCapacitySolid`,
        :obj:`thermo.heat_capacity.HeatCapacityLiquid`,
        and :obj:`thermo.heat_capacity.HeatCapacityGas` to perform the
        actual calculation of each property. Note that those interfaces provide
        output in molar units (J/mol/K).

        Examples
        --------
        >>> w = Chemical('water')
        >>> w.Cp, w.phase
        (4180.597021827336, 'l')
        >>> Chemical('palladium').Cp
        234.26767209171211
        '''
        return phase_select_property(phase=self.phase, s=self.Cps, l=self.Cpl, g=self.Cpg)