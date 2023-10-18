def load_all_methods(self):
        r'''Method which picks out coefficients for the specified chemical
        from the various dictionaries and DataFrames storing it. All data is
        stored as attributes. This method also sets :obj:`Tmin`, :obj:`Tmax`,
        :obj:`all_methods` and obj:`all_methods_P` as a set of methods for
        which the data exists for.

        Called on initialization only. See the source code for the variables at
        which the coefficients are stored. The coefficients can safely be
        altered once the class is initialized. This method can be called again
        to reset the parameters.
        '''
        methods = []
        methods_P = []
        Tmins, Tmaxs = [], []
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP); methods_P.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tt); Tmaxs.append(self.CP_f.Tc)
        if self.CASRN in CRC_inorg_l_data.index:
            methods.append(CRC_INORG_L)
            _, self.CRC_INORG_L_MW, self.CRC_INORG_L_rho, self.CRC_INORG_L_k, self.CRC_INORG_L_Tm, self.CRC_INORG_L_Tmax = _CRC_inorg_l_data_values[CRC_inorg_l_data.index.get_loc(self.CASRN)].tolist()
            Tmins.append(self.CRC_INORG_L_Tm); Tmaxs.append(self.CRC_INORG_L_Tmax)
        if self.CASRN in Perry_l_data.index:
            methods.append(PERRYDIPPR)
            _, C1, C2, C3, C4, self.DIPPR_Tmin, self.DIPPR_Tmax = _Perry_l_data_values[Perry_l_data.index.get_loc(self.CASRN)].tolist()
            self.DIPPR_coeffs = [C1, C2, C3, C4]
            Tmins.append(self.DIPPR_Tmin); Tmaxs.append(self.DIPPR_Tmax)
        if self.CASRN in VDI_PPDS_2.index:
            methods.append(VDI_PPDS)
            _, MW, Tc, rhoc, A, B, C, D = _VDI_PPDS_2_values[VDI_PPDS_2.index.get_loc(self.CASRN)].tolist()
            self.VDI_PPDS_coeffs = [A, B, C, D]
            self.VDI_PPDS_MW = MW
            self.VDI_PPDS_Tc = Tc
            self.VDI_PPDS_rhoc = rhoc
            Tmaxs.append(self.VDI_PPDS_Tc)
        if self.CASRN in _VDISaturationDict:
            methods.append(VDI_TABULAR)
            Ts, props = VDI_tabular_data(self.CASRN, 'Volume (l)')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if self.Tc and self.CASRN in COSTALD_data.index:
            methods.append(HTCOSTALDFIT)
            self.COSTALD_Vchar = float(COSTALD_data.at[self.CASRN, 'Vchar'])
            self.COSTALD_omega_SRK = float(COSTALD_data.at[self.CASRN, 'omega_SRK'])
            Tmins.append(0); Tmaxs.append(self.Tc)
        if self.Tc and self.Pc and self.CASRN in COSTALD_data.index and not np.isnan(COSTALD_data.at[self.CASRN, 'Z_RA']):
            methods.append(RACKETTFIT)
            self.RACKETT_Z_RA = float(COSTALD_data.at[self.CASRN, 'Z_RA'])
            Tmins.append(0); Tmaxs.append(self.Tc)
        if self.CASRN in CRC_inorg_l_const_data.index:
            methods.append(CRC_INORG_L_CONST)
            self.CRC_INORG_L_CONST_Vm = float(CRC_inorg_l_const_data.at[self.CASRN, 'Vm'])
            # Roughly data at STP; not guaranteed however; not used for Trange
        if all((self.Tc, self.Vc, self.Zc)):
            methods.append(YEN_WOODS_SAT)
            Tmins.append(0); Tmaxs.append(self.Tc)
        if all((self.Tc, self.Pc, self.Zc)):
            methods.append(RACKETT)
            Tmins.append(0); Tmaxs.append(self.Tc)
        if all((self.Tc, self.Pc, self.omega)):
            methods.append(YAMADA_GUNN)
            methods.append(BHIRUD_NORMAL)
            Tmins.append(0); Tmaxs.append(self.Tc)
        if all((self.Tc, self.Vc, self.omega)):
            methods.append(TOWNSEND_HALES)
            methods.append(HTCOSTALD)
            methods.append(MMSNM0)
            if self.CASRN in SNM0_data.index:
                methods.append(MMSNM0FIT)
                self.SNM0_delta_SRK = float(SNM0_data.at[self.CASRN, 'delta_SRK'])
            Tmins.append(0); Tmaxs.append(self.Tc)
        if all((self.Tc, self.Vc, self.omega, self.Tb, self.MW)):
            methods.append(CAMPBELL_THODOS)
            Tmins.append(0); Tmaxs.append(self.Tc)
        if all((self.Tc, self.Pc, self.omega)):
            methods_P.append(COSTALD_COMPRESSED)
            if self.eos:
                methods_P.append(EOS)

        if Tmins and Tmaxs:
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)

        self.all_methods = set(methods)
        self.all_methods_P = set(methods_P)