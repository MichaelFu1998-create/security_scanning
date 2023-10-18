def mug(self):
        r'''Viscosity of the mixture in the gas phase at its current
        temperature, pressure, and composition in units of [Pa*s].

        For calculation of this property at other temperatures and pressures,
        or specifying manually the method used to calculate it, and more - see
        the object oriented interface
        :obj:`thermo.viscosity.ViscosityGasMixture`; each Mixture instance
        creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['water'], ws=[1], T=500).mug
        1.7298722343367148e-05
        '''
        return self.ViscosityGasMixture(self.T, self.P, self.zs, self.ws)