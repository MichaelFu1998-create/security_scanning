def nu(self):
        r'''Kinematic viscosity of the the chemical at its current temperature,
        pressure, and phase in units of [m^2/s].

        .. math::
            \nu = \frac{\mu}{\rho}

        Examples
        --------
        >>> Chemical('argon').nu
        1.3846930410865003e-05
        '''
        return phase_select_property(phase=self.phase, l=self.nul, g=self.nug)