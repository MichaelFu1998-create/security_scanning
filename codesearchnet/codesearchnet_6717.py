def Prg(self):
        r'''Prandtl number of the gas phase of the chemical at its
        current temperature and pressure, [dimensionless].

        .. math::
            Pr = \frac{C_p \mu}{k}

        Utilizes the temperature and pressure dependent object oriented
        interfaces :obj:`thermo.viscosity.ViscosityGas`,
        :obj:`thermo.thermal_conductivity.ThermalConductivityGas`,
        and :obj:`thermo.heat_capacity.HeatCapacityGas` to calculate the
        actual properties.

        Examples
        --------
        >>> Chemical('NH3').Prg
        0.847263731933008
        '''
        Cpg, mug, kg = self.Cpg, self.mug, self.kg
        if all([Cpg, mug, kg]):
            return Prandtl(Cp=Cpg, mu=mug, k=kg)
        return None