def alpha(self):
        r'''Thermal diffusivity of the chemical at its current temperature,
        pressure, and phase in units of [m^2/s].

        .. math::
            \alpha = \frac{k}{\rho Cp}

        Examples
        --------
        >>> Chemical('furfural').alpha
        8.696537158635412e-08
        '''
        return phase_select_property(phase=self.phase, l=self.alphal, g=self.alphag)