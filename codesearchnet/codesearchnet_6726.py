def isobaric_expansion(self):
        r'''Isobaric (constant-pressure) expansion of the chemical at its
        current phase and temperature, in units of [1/K].

        .. math::
            \beta = \frac{1}{V}\left(\frac{\partial V}{\partial T} \right)_P

        Examples
        --------
        Radical change  in value just above and below the critical temperature
        of water:

        >>> Chemical('water', T=647.1, P=22048320.0).isobaric_expansion
        0.34074205839222449

        >>> Chemical('water', T=647.2, P=22048320.0).isobaric_expansion
        0.18143324022215077
        '''
        return phase_select_property(phase=self.phase, l=self.isobaric_expansion_l, g=self.isobaric_expansion_g)