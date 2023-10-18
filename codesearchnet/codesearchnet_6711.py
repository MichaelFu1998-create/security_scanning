def JTg(self):
        r'''Joule Thomson coefficient of the chemical in the gas phase at
        its current temperature and pressure, in units of [K/Pa].

        .. math::
            \mu_{JT} = \left(\frac{\partial T}{\partial P}\right)_H = \frac{1}{C_p}
            \left[T \left(\frac{\partial V}{\partial T}\right)_P - V\right]
            = \frac{V}{C_p}\left(\beta T-1\right)

        Utilizes the temperature-derivative method of
        :obj:`thermo.volume.VolumeGas` and the temperature-dependent heat
        capacity method :obj:`thermo.heat_capacity.HeatCapacityGas` to
        obtain the properties required for the actual calculation.

        Examples
        --------
        >>> Chemical('dodecane', T=400, P=1000).JTg
        5.4089897835384913e-05
        '''
        Vmg, Cpgm, isobaric_expansion_g = self.Vmg, self.Cpgm, self.isobaric_expansion_g
        if all((Vmg, Cpgm, isobaric_expansion_g)):
            return Joule_Thomson(T=self.T, V=Vmg, Cp=Cpgm, beta=isobaric_expansion_g)
        return None