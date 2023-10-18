def Cpg(self):
        r'''Gas-phase heat capacity of the chemical at its current temperature,
        in units of [J/kg/K]. For calculation of this property at other
        temperatures, or specifying manually the method used to calculate it,
        and more - see the object oriented interface
        :obj:`thermo.heat_capacity.HeatCapacityGas`; each Chemical instance
        creates one to actually perform the calculations. Note that that
        interface provides output in molar units.

        Examples
        --------
        >>> w = Chemical('water', T=520)
        >>> w.Cpg
        1967.6698314620658
        '''
        Cpgm = self.HeatCapacityGas(self.T)
        if Cpgm:
            return property_molar_to_mass(Cpgm, self.MW)
        return None