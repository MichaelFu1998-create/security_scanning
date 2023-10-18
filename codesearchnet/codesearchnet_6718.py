def solubility_parameter(self):
        r'''Solubility parameter of the chemical at its
        current temperature and pressure, in units of [Pa^0.5].

        .. math::
            \delta = \sqrt{\frac{\Delta H_{vap} - RT}{V_m}}

        Calculated based on enthalpy of vaporization and molar volume.
        Normally calculated at STP. For uses of this property, see
        :obj:`thermo.solubility.solubility_parameter`.

        Examples
        --------
        >>> Chemical('NH3').solubility_parameter
        24766.329043856073
        '''
        return solubility_parameter(T=self.T, Hvapm=self.Hvapm, Vml=self.Vml,
                                    Method=self.solubility_parameter_method,
                                    CASRN=self.CAS)