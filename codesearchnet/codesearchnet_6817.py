def calculate(self, T, method):
        r'''Method to calculate low-pressure liquid molar volume at tempearture
        `T` with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate molar volume, [K]
        method : str
            Name of the method to use

        Returns
        -------
        Vm : float
            Molar volume of the liquid at T and a low pressure, [m^3/mol]
        '''
        if method == RACKETT:
            Vm = Rackett(T, self.Tc, self.Pc, self.Zc)
        elif method == YAMADA_GUNN:
            Vm = Yamada_Gunn(T, self.Tc, self.Pc, self.omega)
        elif method == BHIRUD_NORMAL:
            Vm = Bhirud_normal(T, self.Tc, self.Pc, self.omega)
        elif method == TOWNSEND_HALES:
            Vm = Townsend_Hales(T, self.Tc, self.Vc, self.omega)
        elif method == HTCOSTALD:
            Vm = COSTALD(T, self.Tc, self.Vc, self.omega)
        elif method == YEN_WOODS_SAT:
            Vm = Yen_Woods_saturation(T, self.Tc, self.Vc, self.Zc)
        elif method == MMSNM0:
            Vm = SNM0(T, self.Tc, self.Vc, self.omega)
        elif method == MMSNM0FIT:
            Vm = SNM0(T, self.Tc, self.Vc, self.omega, self.SNM0_delta_SRK)
        elif method == CAMPBELL_THODOS:
            Vm = Campbell_Thodos(T, self.Tb, self.Tc, self.Pc, self.MW, self.dipole)
        elif method == HTCOSTALDFIT:
            Vm = COSTALD(T, self.Tc, self.COSTALD_Vchar, self.COSTALD_omega_SRK)
        elif method == RACKETTFIT:
            Vm = Rackett(T, self.Tc, self.Pc, self.RACKETT_Z_RA)
        elif method == PERRYDIPPR:
            A, B, C, D = self.DIPPR_coeffs
            Vm = 1./EQ105(T, A, B, C, D)
        elif method == CRC_INORG_L:
            rho = CRC_inorganic(T, self.CRC_INORG_L_rho, self.CRC_INORG_L_k, self.CRC_INORG_L_Tm)
            Vm = rho_to_Vm(rho, self.CRC_INORG_L_MW)
        elif method == VDI_PPDS:
            A, B, C, D = self.VDI_PPDS_coeffs
            tau = 1. - T/self.VDI_PPDS_Tc
            rho = self.VDI_PPDS_rhoc + A*tau**0.35 + B*tau**(2/3.) + C*tau + D*tau**(4/3.)
            Vm = rho_to_Vm(rho, self.VDI_PPDS_MW)
        elif method == CRC_INORG_L_CONST:
            Vm = self.CRC_INORG_L_CONST_Vm
        elif method == COOLPROP:
            Vm = 1./CoolProp_T_dependent_property(T, self.CASRN, 'DMOLAR', 'l')
        elif method in self.tabular_data:
            Vm = self.interpolate(T, method)
        return Vm