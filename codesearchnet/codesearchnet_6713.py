def nug(self):
        r'''Kinematic viscosity of the gas phase of the chemical at its
        current temperature and pressure, in units of [m^2/s].

        .. math::
            \nu = \frac{\mu}{\rho}

        Utilizes the temperature and pressure dependent object oriented
        interfaces :obj:`thermo.volume.VolumeGas`,
        :obj:`thermo.viscosity.ViscosityGas`  to calculate the
        actual properties.

        Examples
        --------
        >>> Chemical('methane', T=115).nug
        2.5056924327995865e-06
        '''
        mug, rhog = self.mug, self.rhog
        if all([mug, rhog]):
            return nu_mu_converter(mu=mug, rho=rhog)
        return None