def Cps(self):
        r'''Solid-phase heat capacity of the chemical at its current temperature,
        in units of [J/kg/K]. For calculation of this property at other
        temperatures, or specifying manually the method used to calculate it,
        and more - see the object oriented interface
        :obj:`thermo.heat_capacity.HeatCapacitySolid`; each Chemical instance
        creates one to actually perform the calculations. Note that that
        interface provides output in molar units.

        Examples
        --------
        >>> Chemical('palladium', T=400).Cps
        241.63563239992484
        >>> Pd = Chemical('palladium', T=400)
        >>> Cpsms = [Pd.HeatCapacitySolid.T_dependent_property(T) for T in np.linspace(300,500, 5)]
        >>> [property_molar_to_mass(Cps, Pd.MW) for Cps in Cpsms]
        [234.40150347679008, 238.01856793835751, 241.63563239992484, 245.25269686149224, 248.86976132305958]
        '''
        Cpsm = self.HeatCapacitySolid(self.T)
        if Cpsm:
            return property_molar_to_mass(Cpsm, self.MW)
        return None