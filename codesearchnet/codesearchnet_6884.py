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
        if self.CASRN in Mulero_Cachadina_data.index:
            methods.append(STREFPROP)
            _, sigma0, n0, sigma1, n1, sigma2, n2, Tc, self.STREFPROP_Tmin, self.STREFPROP_Tmax = _Mulero_Cachadina_data_values[Mulero_Cachadina_data.index.get_loc(self.CASRN)].tolist()
            self.STREFPROP_coeffs = [sigma0, n0, sigma1, n1, sigma2, n2, Tc]
            Tmins.append(self.STREFPROP_Tmin); Tmaxs.append(self.STREFPROP_Tmax)
        if self.CASRN in Somayajulu_data_2.index:
            methods.append(SOMAYAJULU2)
            _, self.SOMAYAJULU2_Tt, self.SOMAYAJULU2_Tc, A, B, C = _Somayajulu_data_2_values[Somayajulu_data_2.index.get_loc(self.CASRN)].tolist()
            self.SOMAYAJULU2_coeffs = [A, B, C]
            Tmins.append(self.SOMAYAJULU2_Tt); Tmaxs.append(self.SOMAYAJULU2_Tc)
        if self.CASRN in Somayajulu_data.index:
            methods.append(SOMAYAJULU)
            _, self.SOMAYAJULU_Tt, self.SOMAYAJULU_Tc, A, B, C = _Somayajulu_data_values[Somayajulu_data.index.get_loc(self.CASRN)].tolist()
            self.SOMAYAJULU_coeffs = [A, B, C]
            Tmins.append(self.SOMAYAJULU_Tt); Tmaxs.append(self.SOMAYAJULU_Tc)
        if self.CASRN in _VDISaturationDict:
            methods.append(VDI_TABULAR)
            Ts, props = VDI_tabular_data(self.CASRN, 'sigma')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if self.CASRN in Jasper_Lange_data.index:
            methods.append(JASPER)
            _, a, b, self.JASPER_Tmin, self.JASPER_Tmax= _Jasper_Lange_data_values[Jasper_Lange_data.index.get_loc(self.CASRN)].tolist()
            self.JASPER_coeffs = [a, b]
            Tmins.append(self.JASPER_Tmin); Tmaxs.append(self.JASPER_Tmax)
        if all((self.Tc, self.Vc, self.omega)):
            methods.append(MIQUEU)
            Tmins.append(0.0); Tmaxs.append(self.Tc)
        if all((self.Tb, self.Tc, self.Pc)):
            methods.append(BROCK_BIRD)
            methods.append(SASTRI_RAO)
            Tmins.append(0.0); Tmaxs.append(self.Tc)
        if all((self.Tc, self.Pc, self.omega)):
            methods.append(PITZER)
            methods.append(ZUO_STENBY)
            Tmins.append(0.0); Tmaxs.append(self.Tc)
        if self.CASRN in VDI_PPDS_11.index:
            _,  Tm, Tc, A, B, C, D, E = _VDI_PPDS_11_values[VDI_PPDS_11.index.get_loc(self.CASRN)].tolist()
            self.VDI_PPDS_coeffs = [A, B, C, D, E]
            self.VDI_PPDS_Tc = Tc
            self.VDI_PPDS_Tm = Tm
            methods.append(VDI_PPDS)
            Tmins.append(self.VDI_PPDS_Tm) ; Tmaxs.append(self.VDI_PPDS_Tc); 
        if all((self.Tb, self.Hvap_Tb, self.MW)):
            # Cache Cpl at Tb for ease of calculation of Tmax
            self.Cpl_Tb = self.Cpl(self.Tb) if hasattr(self.Cpl, '__call__') else self.Cpl
            if self.Cpl_Tb:
                methods.append(ALEEM)
                # Tmin and Tmax for this method is known
                Tmax_possible = self.Tb + self.Hvap_Tb/self.Cpl_Tb
                # This method will ruin solve_prop as it is typically valid
                # well above Tc. If Tc is available, limit it to that.
                if self.Tc:
                    Tmax_possible = min(self.Tc, Tmax_possible)
                Tmins.append(0.0); Tmaxs.append(Tmax_possible)
        self.all_methods = set(methods)
        if Tmins and Tmaxs:
            # Note: All methods work right down to 0 K.
            self.Tmin = min(Tmins)
            self.Tmax = max(Tmaxs)