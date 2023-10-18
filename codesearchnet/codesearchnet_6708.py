def isobaric_expansion_l(self):
        r'''Isobaric (constant-pressure) expansion of the liquid phase of the
        chemical at its current temperature and pressure, in units of [1/K].

        .. math::
            \beta = \frac{1}{V}\left(\frac{\partial V}{\partial T} \right)_P

        Utilizes the temperature-derivative method of
        :obj:`thermo.volume.VolumeLiquid` to perform the actual calculation.
        The derivatives are all numerical.

        Examples
        --------
        >>> Chemical('dodecane', T=400).isobaric_expansion_l
        0.0011617555762469477
        '''
        dV_dT = self.VolumeLiquid.TP_dependent_property_derivative_T(self.T, self.P)
        Vm = self.Vml
        if dV_dT and Vm:
            return isobaric_expansion(V=Vm, dV_dT=dV_dT)