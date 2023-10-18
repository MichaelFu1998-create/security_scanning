def alphag(self):
        r'''Thermal diffusivity of the gas phase of the chemical at its
        current temperature and pressure, in units of [m^2/s].

        .. math::
            \alpha = \frac{k}{\rho Cp}

        Utilizes the temperature and pressure dependent object oriented
        interfaces :obj:`thermo.volume.VolumeGas`,
        :obj:`thermo.thermal_conductivity.ThermalConductivityGas`,
        and :obj:`thermo.heat_capacity.HeatCapacityGas` to calculate the
        actual properties.

        Examples
        --------
        >>> Chemical('ammonia').alphag
        1.6931865425158556e-05
        '''
        kg, rhog, Cpg = self.kg, self.rhog, self.Cpg
        if all([kg, rhog, Cpg]):
            return thermal_diffusivity(k=kg, rho=rhog, Cp=Cpg)
        return None