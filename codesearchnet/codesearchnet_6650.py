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
        if self.CASRN in zabransky_dict_const_s:
            methods.append(ZABRANSKY_SPLINE)
            self.Zabransky_spline = zabransky_dict_const_s[self.CASRN]
        if self.CASRN in zabransky_dict_const_p:
            methods.append(ZABRANSKY_QUASIPOLYNOMIAL)
            self.Zabransky_quasipolynomial = zabransky_dict_const_p[self.CASRN]
        if self.CASRN in zabransky_dict_iso_s:
            methods.append(ZABRANSKY_SPLINE_C)
            self.Zabransky_spline_iso = zabransky_dict_iso_s[self.CASRN]
        if self.CASRN in zabransky_dict_iso_p:
            methods.append(ZABRANSKY_QUASIPOLYNOMIAL_C)
            self.Zabransky_quasipolynomial_iso = zabransky_dict_iso_p[self.CASRN]
        if self.CASRN in Poling_data.index and not np.isnan(Poling_data.at[self.CASRN, 'Cpl']):
            methods.append(POLING_CONST)
            self.POLING_T = 298.15
            self.POLING_constant = float(Poling_data.at[self.CASRN, 'Cpl'])
        if self.CASRN in CRC_standard_data.index and not np.isnan(CRC_standard_data.at[self.CASRN, 'Cpl']):
            methods.append(CRCSTD)
            self.CRCSTD_T = 298.15
            self.CRCSTD_constant = float(CRC_standard_data.at[self.CASRN, 'Cpl'])
        # Saturation functions
        if self.CASRN in zabransky_dict_sat_s:
            methods.append(ZABRANSKY_SPLINE_SAT)
            self.Zabransky_spline_sat = zabransky_dict_sat_s[self.CASRN]
        if self.CASRN in zabransky_dict_sat_p:
            methods.append(ZABRANSKY_QUASIPOLYNOMIAL_SAT)
            self.Zabransky_quasipolynomial_sat = zabransky_dict_sat_p[self.CASRN]
        if self.CASRN in _VDISaturationDict:
            # NOTE: VDI data is for the saturation curve, i.e. at increasing
            # pressure; it is normally substantially higher than the ideal gas
            # value
            methods.append(VDI_TABULAR)
            Ts, props = VDI_tabular_data(self.CASRN, 'Cp (l)')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if self.Tc and self.omega:
            methods.extend([ROWLINSON_POLING, ROWLINSON_BONDI])
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tt); Tmaxs.append(self.CP_f.Tc)
        if self.MW and self.similarity_variable:
            methods.append(DADGOSTAR_SHAW)
        self.all_methods = set(methods)
        if Tmins and Tmaxs:
            # TODO: More Tmin, Tmax ranges
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)