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
        if self.CASRN in TRC_gas_data.index:
            methods.append(TRCIG)
            _, self.TRCIG_Tmin, self.TRCIG_Tmax, a0, a1, a2, a3, a4, a5, a6, a7, _, _, _ = _TRC_gas_data_values[TRC_gas_data.index.get_loc(self.CASRN)].tolist()
            self.TRCIG_coefs = [a0, a1, a2, a3, a4, a5, a6, a7]
            Tmins.append(self.TRCIG_Tmin); Tmaxs.append(self.TRCIG_Tmax)
        if self.CASRN in Poling_data.index and not np.isnan(Poling_data.at[self.CASRN, 'a0']):
            _, self.POLING_Tmin, self.POLING_Tmax, a0, a1, a2, a3, a4, Cpg, Cpl = _Poling_data_values[Poling_data.index.get_loc(self.CASRN)].tolist()
            methods.append(POLING)
            self.POLING_coefs = [a0, a1, a2, a3, a4]
            Tmins.append(self.POLING_Tmin); Tmaxs.append(self.POLING_Tmax)
        if self.CASRN in Poling_data.index and not np.isnan(Poling_data.at[self.CASRN, 'Cpg']):
            methods.append(POLING_CONST)
            self.POLING_T = 298.15
            self.POLING_constant = float(Poling_data.at[self.CASRN, 'Cpg'])
        if self.CASRN in CRC_standard_data.index and not np.isnan(CRC_standard_data.at[self.CASRN, 'Cpg']):
            methods.append(CRCSTD)
            self.CRCSTD_T = 298.15
            self.CRCSTD_constant = float(CRC_standard_data.at[self.CASRN, 'Cpg'])
        if self.CASRN in _VDISaturationDict:
            # NOTE: VDI data is for the saturation curve, i.e. at increasing
            # pressure; it is normally substantially higher than the ideal gas
            # value
            methods.append(VDI_TABULAR)
            Ts, props = VDI_tabular_data(self.CASRN, 'Cp (g)')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tt); Tmaxs.append(self.CP_f.Tc)
        if self.MW and self.similarity_variable:
            methods.append(LASTOVKA_SHAW)
        self.all_methods = set(methods)
        if Tmins and Tmaxs:
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)