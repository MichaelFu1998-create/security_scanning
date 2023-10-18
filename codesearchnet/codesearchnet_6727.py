def JT(self):
        r'''Joule Thomson coefficient of the chemical at its
        current phase and temperature, in units of [K/Pa].

        .. math::
            \mu_{JT} = \left(\frac{\partial T}{\partial P}\right)_H = \frac{1}{C_p}
            \left[T \left(\frac{\partial V}{\partial T}\right)_P - V\right]
            = \frac{V}{C_p}\left(\beta T-1\right)

        Examples
        --------
        >>> Chemical('water').JT
        -2.2150394958666407e-07
        '''
        return phase_select_property(phase=self.phase, l=self.JTl, g=self.JTg)