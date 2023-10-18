def load_all_methods(self):
        r'''Method which picks out coefficients for the specified chemical
        from the various dictionaries and DataFrames storing it. All data is
        stored as attributes. This method also sets :obj:`Tmin`, :obj:`Tmax`,
        and :obj:`all_methods` as a set of methods for which the data exists for.

        Called on initialization only. See the source code for the variables at
        which the coefficients are stored. The coefficients can safely be
        altered once the class is initialized. This method can be called again
        to reset the parameters.
        '''
        methods = []
        Tmins, Tmaxs = [], []
        if self.CASRN in WagnerMcGarry.index:
            methods.append(WAGNER_MCGARRY)
            _, A, B, C, D, self.WAGNER_MCGARRY_Pc, self.WAGNER_MCGARRY_Tc, self.WAGNER_MCGARRY_Tmin = _WagnerMcGarry_values[WagnerMcGarry.index.get_loc(self.CASRN)].tolist()
            self.WAGNER_MCGARRY_coefs = [A, B, C, D]
            Tmins.append(self.WAGNER_MCGARRY_Tmin); Tmaxs.append(self.WAGNER_MCGARRY_Tc)
        if self.CASRN in WagnerPoling.index:
            methods.append(WAGNER_POLING)
            _, A, B, C, D, self.WAGNER_POLING_Tc, self.WAGNER_POLING_Pc, Tmin, self.WAGNER_POLING_Tmax = _WagnerPoling_values[WagnerPoling.index.get_loc(self.CASRN)].tolist()
            # Some Tmin values are missing; Arbitrary choice of 0.1 lower limit
            self.WAGNER_POLING_Tmin = Tmin if not np.isnan(Tmin) else self.WAGNER_POLING_Tmax*0.1
            self.WAGNER_POLING_coefs = [A, B, C, D]
            Tmins.append(Tmin); Tmaxs.append(self.WAGNER_POLING_Tmax)
        if self.CASRN in AntoineExtended.index:
            methods.append(ANTOINE_EXTENDED_POLING)
            _, A, B, C, Tc, to, n, E, F, self.ANTOINE_EXTENDED_POLING_Tmin, self.ANTOINE_EXTENDED_POLING_Tmax = _AntoineExtended_values[AntoineExtended.index.get_loc(self.CASRN)].tolist()
            self.ANTOINE_EXTENDED_POLING_coefs = [Tc, to, A, B, C, n, E, F]
            Tmins.append(self.ANTOINE_EXTENDED_POLING_Tmin); Tmaxs.append(self.ANTOINE_EXTENDED_POLING_Tmax)
        if self.CASRN in AntoinePoling.index:
            methods.append(ANTOINE_POLING)
            _, A, B, C, self.ANTOINE_POLING_Tmin, self.ANTOINE_POLING_Tmax = _AntoinePoling_values[AntoinePoling.index.get_loc(self.CASRN)].tolist()
            self.ANTOINE_POLING_coefs = [A, B, C]
            Tmins.append(self.ANTOINE_POLING_Tmin); Tmaxs.append(self.ANTOINE_POLING_Tmax)
        if self.CASRN in Perrys2_8.index:
            methods.append(DIPPR_PERRY_8E)
            _, C1, C2, C3, C4, C5, self.Perrys2_8_Tmin, self.Perrys2_8_Tmax = _Perrys2_8_values[Perrys2_8.index.get_loc(self.CASRN)].tolist()
            self.Perrys2_8_coeffs = [C1, C2, C3, C4, C5]
            Tmins.append(self.Perrys2_8_Tmin); Tmaxs.append(self.Perrys2_8_Tmax)
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tmin); Tmaxs.append(self.CP_f.Tc)
        if self.CASRN in _VDISaturationDict:
            methods.append(VDI_TABULAR)
            Ts, props = VDI_tabular_data(self.CASRN, 'P')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if self.CASRN in VDI_PPDS_3.index:
            _,  Tm, Tc, Pc, A, B, C, D = _VDI_PPDS_3_values[VDI_PPDS_3.index.get_loc(self.CASRN)].tolist()
            self.VDI_PPDS_coeffs = [A, B, C, D]
            self.VDI_PPDS_Tc = Tc
            self.VDI_PPDS_Tm = Tm
            self.VDI_PPDS_Pc = Pc
            methods.append(VDI_PPDS)
            Tmins.append(self.VDI_PPDS_Tm); Tmaxs.append(self.VDI_PPDS_Tc)
        if all((self.Tb, self.Tc, self.Pc)):
            methods.append(BOILING_CRITICAL)
            Tmins.append(0.01); Tmaxs.append(self.Tc)
        if all((self.Tc, self.Pc, self.omega)):
            methods.append(LEE_KESLER_PSAT)
            methods.append(AMBROSE_WALTON)
            methods.append(SANJARI)
            methods.append(EDALAT)
            if self.eos:
                methods.append(EOS)
            Tmins.append(0.01); Tmaxs.append(self.Tc)
        self.all_methods = set(methods)
        if Tmins and Tmaxs:
            self.Tmin = min(Tmins)
            self.Tmax = max(Tmaxs)