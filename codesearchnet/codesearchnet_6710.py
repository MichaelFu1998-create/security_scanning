def JTl(self):
        r'''Joule Thomson coefficient of the chemical in the liquid phase at
        its current temperature and pressure, in units of [K/Pa].

        .. math::
            \mu_{JT} = \left(\frac{\partial T}{\partial P}\right)_H = \frac{1}{C_p}
            \left[T \left(\frac{\partial V}{\partial T}\right)_P - V\right]
            = \frac{V}{C_p}\left(\beta T-1\right)

        Utilizes the temperature-derivative method of
        :obj:`thermo.volume.VolumeLiquid` and the temperature-dependent heat
        capacity method :obj:`thermo.heat_capacity.HeatCapacityLiquid` to
        obtain the properties required for the actual calculation.

        Examples
        --------
        >>> Chemical('dodecane', T=400).JTl
        -3.0827160465192742e-07
        '''
        Vml, Cplm, isobaric_expansion_l = self.Vml, self.Cplm, self.isobaric_expansion_l
        if all((Vml, Cplm, isobaric_expansion_l)):
            return Joule_Thomson(T=self.T, V=Vml, Cp=Cplm, beta=isobaric_expansion_l)
        return None