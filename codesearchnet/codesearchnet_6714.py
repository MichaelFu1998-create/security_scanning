def alphal(self):
        r'''Thermal diffusivity of the liquid phase of the chemical at its
        current temperature and pressure, in units of [m^2/s].

        .. math::
            \alpha = \frac{k}{\rho Cp}

        Utilizes the temperature and pressure dependent object oriented
        interfaces :obj:`thermo.volume.VolumeLiquid`,
        :obj:`thermo.thermal_conductivity.ThermalConductivityLiquid`,
        and :obj:`thermo.heat_capacity.HeatCapacityLiquid` to calculate the
        actual properties.

        Examples
        --------
        >>> Chemical('nitrogen', T=70).alphal
        9.444949636299626e-08
        '''
        kl, rhol, Cpl = self.kl, self.rhol, self.Cpl
        if all([kl, rhol, Cpl]):
            return thermal_diffusivity(k=kl, rho=rhol, Cp=Cpl)
        return None