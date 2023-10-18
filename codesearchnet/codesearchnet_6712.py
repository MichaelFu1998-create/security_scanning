def nul(self):
        r'''Kinematic viscosity of the liquid phase of the chemical at its
        current temperature and pressure, in units of [m^2/s].

        .. math::
            \nu = \frac{\mu}{\rho}

        Utilizes the temperature and pressure dependent object oriented
        interfaces :obj:`thermo.volume.VolumeLiquid`,
        :obj:`thermo.viscosity.ViscosityLiquid`  to calculate the
        actual properties.

        Examples
        --------
        >>> Chemical('methane', T=110).nul
        2.858088468937331e-07
        '''
        mul, rhol = self.mul, self.rhol
        if all([mul, rhol]):
            return nu_mu_converter(mu=mul, rho=rhol)
        return None