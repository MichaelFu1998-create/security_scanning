def kg(self):
        r'''Thermal conductivity of the mixture in the gas phase at its current
        temperature, pressure, and composition in units of [Pa*s].

        For calculation of this property at other temperatures and pressures,
        or specifying manually the method used to calculate it, and more - see
        the object oriented interface
        :obj:`thermo.thermal_conductivity.ThermalConductivityGasMixture`;
        each Mixture instance creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['water'], ws=[1], T=500).kg
        0.036035173297862676
        '''
        return self.ThermalConductivityGasMixture(self.T, self.P, self.zs, self.ws)