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
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tt); Tmaxs.append(self.CP_f.Tc)
        if self.CASRN in _VDISaturationDict:
            methods.append(VDI_TABULAR)
            Ts, props = VDI_tabular_data(self.CASRN, 'Hvap')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if self.CASRN in Alibakhshi_Cs.index and self.Tc:
            methods.append(ALIBAKHSHI)
            self.Alibakhshi_C = float(Alibakhshi_Cs.at[self.CASRN, 'C'])
            Tmaxs.append( max(self.Tc-100., 0) )
        if self.CASRN in CRCHvap_data.index and not np.isnan(CRCHvap_data.at[self.CASRN, 'HvapTb']):
            methods.append(CRC_HVAP_TB)
            self.CRC_HVAP_TB_Tb = float(CRCHvap_data.at[self.CASRN, 'Tb'])
            self.CRC_HVAP_TB_Hvap = float(CRCHvap_data.at[self.CASRN, 'HvapTb'])
        if self.CASRN in CRCHvap_data.index and not np.isnan(CRCHvap_data.at[self.CASRN, 'Hvap298']):
            methods.append(CRC_HVAP_298)
            self.CRC_HVAP_298 = float(CRCHvap_data.at[self.CASRN, 'Hvap298'])
        if self.CASRN in GharagheiziHvap_data.index:
            methods.append(GHARAGHEIZI_HVAP_298)
            self.GHARAGHEIZI_HVAP_298_Hvap = float(GharagheiziHvap_data.at[self.CASRN, 'Hvap298'])
        if all((self.Tc, self.omega)):
            methods.extend(self.CSP_methods)
            Tmaxs.append(self.Tc); Tmins.append(0)
        if all((self.Tc, self.Pc)):
            methods.append(CLAPEYRON)
            Tmaxs.append(self.Tc); Tmins.append(0)
        if all((self.Tb, self.Tc, self.Pc)):
            methods.extend(self.boiling_methods)
            Tmaxs.append(self.Tc); Tmins.append(0)
        if self.CASRN in Perrys2_150.index:
            methods.append(DIPPR_PERRY_8E)
            _, Tc, C1, C2, C3, C4, self.Perrys2_150_Tmin, self.Perrys2_150_Tmax = _Perrys2_150_values[Perrys2_150.index.get_loc(self.CASRN)].tolist()
            self.Perrys2_150_coeffs = [Tc, C1, C2, C3, C4]
            Tmins.append(self.Perrys2_150_Tmin); Tmaxs.append(self.Perrys2_150_Tmax)
        if self.CASRN in VDI_PPDS_4.index:
            _,  MW, Tc, A, B, C, D, E = _VDI_PPDS_4_values[VDI_PPDS_4.index.get_loc(self.CASRN)].tolist()
            self.VDI_PPDS_coeffs = [A, B, C, D, E]
            self.VDI_PPDS_Tc = Tc
            self.VDI_PPDS_MW = MW
            methods.append(VDI_PPDS)
            Tmaxs.append(self.VDI_PPDS_Tc); 
        self.all_methods = set(methods)
        if Tmins and Tmaxs:
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)