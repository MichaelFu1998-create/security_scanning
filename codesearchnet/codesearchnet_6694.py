def Cpl(self):
        r'''Liquid-phase heat capacity of the chemical at its current temperature,
        in units of [J/kg/K]. For calculation of this property at other
        temperatures, or specifying manually the method used to calculate it,
        and more - see the object oriented interface
        :obj:`thermo.heat_capacity.HeatCapacityLiquid`; each Chemical instance
        creates one to actually perform the calculations. Note that that
        interface provides output in molar units.

        Examples
        --------
        >>> Chemical('water', T=320).Cpl
        4177.518996988284

        Ideal entropy change of water from 280 K to 340 K, output converted
        back to mass-based units of J/kg/K.

        >>> dSm = Chemical('water').HeatCapacityLiquid.T_dependent_property_integral_over_T(280, 340)
        >>> property_molar_to_mass(dSm, Chemical('water').MW)
        812.1024585274956
        '''
        Cplm = self.HeatCapacityLiquid(self.T)
        if Cplm:
            return property_molar_to_mass(Cplm, self.MW)
        return None