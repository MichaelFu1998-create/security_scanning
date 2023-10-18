def calculate(self, T, method):
        r'''Method to calculate surface tension of a liquid at temperature `T`
        with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate surface tension, [K]
        method : str
            Name of the method to use

        Returns
        -------
        sigma : float
            Surface tension of the liquid at T, [N/m]
        '''
        if method == STREFPROP:
            sigma0, n0, sigma1, n1, sigma2, n2, Tc = self.STREFPROP_coeffs
            sigma = REFPROP(T, Tc=Tc, sigma0=sigma0, n0=n0, sigma1=sigma1, n1=n1,
                            sigma2=sigma2, n2=n2)
        elif method == VDI_PPDS:
            sigma = EQ106(T, self.VDI_PPDS_Tc, *self.VDI_PPDS_coeffs)
        elif method == SOMAYAJULU2:
            A, B, C = self.SOMAYAJULU2_coeffs
            sigma = Somayajulu(T, Tc=self.SOMAYAJULU2_Tc, A=A, B=B, C=C)
        elif method == SOMAYAJULU:
            A, B, C = self.SOMAYAJULU_coeffs
            sigma = Somayajulu(T, Tc=self.SOMAYAJULU_Tc, A=A, B=B, C=C)
        elif method == JASPER:
            sigma = Jasper(T, a=self.JASPER_coeffs[0], b=self.JASPER_coeffs[1])
        elif method == BROCK_BIRD:
            sigma = Brock_Bird(T, self.Tb, self.Tc, self.Pc)
        elif method == SASTRI_RAO:
            sigma = Sastri_Rao(T, self.Tb, self.Tc, self.Pc)
        elif method == PITZER:
            sigma = Pitzer(T, self.Tc, self.Pc, self.omega)
        elif method == ZUO_STENBY:
            sigma = Zuo_Stenby(T, self.Tc, self.Pc, self.omega)
        elif method == MIQUEU:
            sigma = Miqueu(T, self.Tc, self.Vc, self.omega)
        elif method == ALEEM:
            Cpl = self.Cpl(T) if hasattr(self.Cpl, '__call__') else self.Cpl
            Vml = self.Vml(T) if hasattr(self.Vml, '__call__') else self.Vml
            rhol = Vm_to_rho(Vml, self.MW)
            sigma = Aleem(T=T, MW=self.MW, Tb=self.Tb, rhol=rhol, Hvap_Tb=self.Hvap_Tb, Cpl=Cpl)
        elif method in self.tabular_data:
            sigma = self.interpolate(T, method)
        return sigma