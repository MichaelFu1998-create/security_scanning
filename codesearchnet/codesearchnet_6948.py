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
        methods, methods_P = [], []
        Tmins, Tmaxs = [], []
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP); methods_P.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tmin); Tmaxs.append(self.CP_f.Tc)
        if self.CASRN in _VDISaturationDict:
            methods.append(VDI_TABULAR)
            Ts, props = VDI_tabular_data(self.CASRN, 'Mu (l)')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if self.CASRN in Dutt_Prasad.index:
            methods.append(DUTT_PRASAD)
            _, A, B, C, self.DUTT_PRASAD_Tmin, self.DUTT_PRASAD_Tmax = _Dutt_Prasad_values[Dutt_Prasad.index.get_loc(self.CASRN)].tolist()
            self.DUTT_PRASAD_coeffs = [A, B, C]
            Tmins.append(self.DUTT_PRASAD_Tmin); Tmaxs.append(self.DUTT_PRASAD_Tmax)
        if self.CASRN in VN3_data.index:
            methods.append(VISWANATH_NATARAJAN_3)
            _, _, A, B, C, self.VISWANATH_NATARAJAN_3_Tmin, self.VISWANATH_NATARAJAN_3_Tmax = _VN3_data_values[VN3_data.index.get_loc(self.CASRN)].tolist()
            self.VISWANATH_NATARAJAN_3_coeffs = [A, B, C]
            Tmins.append(self.VISWANATH_NATARAJAN_3_Tmin); Tmaxs.append(self.VISWANATH_NATARAJAN_3_Tmax)
        if self.CASRN in VN2_data.index:
            methods.append(VISWANATH_NATARAJAN_2)
            _, _, A, B, self.VISWANATH_NATARAJAN_2_Tmin, self.VISWANATH_NATARAJAN_2_Tmax = _VN2_data_values[VN2_data.index.get_loc(self.CASRN)].tolist()
            self.VISWANATH_NATARAJAN_2_coeffs = [A, B]
            Tmins.append(self.VISWANATH_NATARAJAN_2_Tmin); Tmaxs.append(self.VISWANATH_NATARAJAN_2_Tmax)
        if self.CASRN in VN2E_data.index:
            methods.append(VISWANATH_NATARAJAN_2E)
            _, _, C, D, self.VISWANATH_NATARAJAN_2E_Tmin, self.VISWANATH_NATARAJAN_2E_Tmax = _VN2E_data_values[VN2E_data.index.get_loc(self.CASRN)].tolist()
            self.VISWANATH_NATARAJAN_2E_coeffs = [C, D]
            Tmins.append(self.VISWANATH_NATARAJAN_2E_Tmin); Tmaxs.append(self.VISWANATH_NATARAJAN_2E_Tmax)
        if self.CASRN in Perrys2_313.index:
            methods.append(DIPPR_PERRY_8E)
            _, C1, C2, C3, C4, C5, self.Perrys2_313_Tmin, self.Perrys2_313_Tmax = _Perrys2_313_values[Perrys2_313.index.get_loc(self.CASRN)].tolist()
            self.Perrys2_313_coeffs = [C1, C2, C3, C4, C5]
            Tmins.append(self.Perrys2_313_Tmin); Tmaxs.append(self.Perrys2_313_Tmax)
        if self.CASRN in VDI_PPDS_7.index:
            methods.append(VDI_PPDS)
            self.VDI_PPDS_coeffs = _VDI_PPDS_7_values[VDI_PPDS_7.index.get_loc(self.CASRN)].tolist()[2:]
        if all((self.MW, self.Tc, self.Pc, self.omega)):
            methods.append(LETSOU_STIEL)
            Tmins.append(self.Tc/4); Tmaxs.append(self.Tc) # TODO: test model at low T
        if all((self.MW, self.Tm, self.Tc, self.Pc, self.Vc, self.omega, self.Vml)):
            methods.append(PRZEDZIECKI_SRIDHAR)
            Tmins.append(self.Tm); Tmaxs.append(self.Tc) # TODO: test model at Tm
        if all([self.Tc, self.Pc, self.omega]):
            methods_P.append(LUCAS)
        self.all_methods = set(methods)
        self.all_methods_P = set(methods_P)
        if Tmins and Tmaxs:
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)