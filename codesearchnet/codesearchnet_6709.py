def isobaric_expansion_g(self):
        r'''Isobaric (constant-pressure) expansion of the gas phase of the
        chemical at its current temperature and pressure, in units of [1/K].

        .. math::
            \beta = \frac{1}{V}\left(\frac{\partial V}{\partial T} \right)_P

        Utilizes the temperature-derivative method of
        :obj:`thermo.VolumeGas` to perform the actual calculation.
        The derivatives are all numerical.

        Examples
        --------
        >>> Chemical('Hexachlorobenzene', T=900).isobaric_expansion_g
        0.001151869741981048
        '''
        dV_dT = self.VolumeGas.TP_dependent_property_derivative_T(self.T, self.P)
        Vm = self.Vmg
        if dV_dT and Vm:
            return isobaric_expansion(V=Vm, dV_dT=dV_dT)