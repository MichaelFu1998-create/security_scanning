def calculate(self, T, method):
        r'''Method to calculate heat of vaporization of a liquid at
        temperature `T` with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate heat of vaporization, [K]
        method : str
            Name of the method to use

        Returns
        -------
        Hvap : float
            Heat of vaporization of the liquid at T, [J/mol]
        '''
        if method == COOLPROP:
            Hvap = PropsSI('HMOLAR', 'T', T, 'Q', 1, self.CASRN) - PropsSI('HMOLAR', 'T', T, 'Q', 0, self.CASRN)
        elif method == DIPPR_PERRY_8E:
            Hvap = EQ106(T, *self.Perrys2_150_coeffs)
        # CSP methods
        elif method == VDI_PPDS:
            A, B, C, D, E = self.VDI_PPDS_coeffs
            tau = 1. - T/self.VDI_PPDS_Tc
            Hvap = R*self.VDI_PPDS_Tc*(A*tau**(1/3.) + B*tau**(2/3.) + C*tau
                                       + D*tau**2 + E*tau**6)
        elif method == ALIBAKHSHI:
            Hvap = (4.5*pi*N_A)**(1/3.)*4.2E-7*(self.Tc-6.) - R/2.*T*log(T) + self.Alibakhshi_C*T
        elif method == MORGAN_KOBAYASHI:
            Hvap = MK(T, self.Tc, self.omega)
        elif method == SIVARAMAN_MAGEE_KOBAYASHI:
            Hvap = SMK(T, self.Tc, self.omega)
        elif method == VELASCO:
            Hvap = Velasco(T, self.Tc, self.omega)
        elif method == PITZER:
            Hvap = Pitzer(T, self.Tc, self.omega)
        elif method == CLAPEYRON:
            Zg = self.Zg(T) if hasattr(self.Zg, '__call__') else self.Zg
            Zl = self.Zl(T) if hasattr(self.Zl, '__call__') else self.Zl
            Psat = self.Psat(T) if hasattr(self.Psat, '__call__') else self.Psat
            if Zg:
                if Zl:
                    dZ = Zg-Zl
                else:
                    dZ = Zg
            Hvap = Clapeyron(T, self.Tc, self.Pc, dZ=dZ, Psat=Psat)
        # CSP methods at Tb only
        elif method == RIEDEL:
            Hvap = Riedel(self.Tb, self.Tc, self.Pc)
        elif method == CHEN:
            Hvap = Chen(self.Tb, self.Tc, self.Pc)
        elif method == VETERE:
            Hvap = Vetere(self.Tb, self.Tc, self.Pc)
        elif method == LIU:
            Hvap = Liu(self.Tb, self.Tc, self.Pc)
        # Individual data point methods
        elif method == CRC_HVAP_TB:
            Hvap = self.CRC_HVAP_TB_Hvap
        elif method == CRC_HVAP_298:
            Hvap = self.CRC_HVAP_298
        elif method == GHARAGHEIZI_HVAP_298:
            Hvap = self.GHARAGHEIZI_HVAP_298_Hvap
        elif method in self.tabular_data:
            Hvap = self.interpolate(T, method)
        # Adjust with the watson equation if estimated at Tb or Tc only
        if method in self.boiling_methods or (self.Tc and method in [CRC_HVAP_TB, CRC_HVAP_298, GHARAGHEIZI_HVAP_298]):
            if method in self.boiling_methods:
                Tref = self.Tb
            elif method == CRC_HVAP_TB:
                Tref = self.CRC_HVAP_TB_Tb
            elif method in [CRC_HVAP_298, GHARAGHEIZI_HVAP_298]:
                Tref = 298.15
            Hvap = Watson(T, Hvap, Tref, self.Tc, self.Watson_exponent)
        return Hvap