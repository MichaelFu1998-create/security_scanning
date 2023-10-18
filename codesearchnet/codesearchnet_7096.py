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
        if self.CASRN in _VDISaturationDict:
            methods.append(VDI_TABULAR)
            Ts, props = VDI_tabular_data(self.CASRN, 'K (l)')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP); methods_P.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tmin); Tmaxs.append(self.CP_f.Tc)
        if self.MW:
            methods.extend([BAHADORI_L, LAKSHMI_PRASAD])
            # Tmin and Tmax are not extended by these simple models, who often
            # give values of 0; BAHADORI_L even has 3 roots.
            # LAKSHMI_PRASAD works down to 0 K, and has an upper limit of
            # 50.0*(131.0*sqrt(M) + 2771.0)/(50.0*M**0.5 + 197.0)
            # where it becomes 0.
        if self.CASRN in Perrys2_315.index:
            methods.append(DIPPR_PERRY_8E)
            _, C1, C2, C3, C4, C5, self.Perrys2_315_Tmin, self.Perrys2_315_Tmax = _Perrys2_315_values[Perrys2_315.index.get_loc(self.CASRN)].tolist()
            self.Perrys2_315_coeffs = [C1, C2, C3, C4, C5]
            Tmins.append(self.Perrys2_315_Tmin); Tmaxs.append(self.Perrys2_315_Tmax)
        if self.CASRN in VDI_PPDS_9.index:
            _,  A, B, C, D, E = _VDI_PPDS_9_values[VDI_PPDS_9.index.get_loc(self.CASRN)].tolist()
            self.VDI_PPDS_coeffs = [A, B, C, D, E]
            self.VDI_PPDS_coeffs.reverse()
            methods.append(VDI_PPDS)
        if all([self.MW, self.Tm]):
            methods.append(SHEFFY_JOHNSON)
            Tmins.append(0); Tmaxs.append(self.Tm + 793.65)
            # Works down to 0, has a nice limit at T = Tm+793.65 from Sympy
        if all([self.Tb, self.Pc, self.omega]):
            methods.append(GHARAGHEIZI_L)
            Tmins.append(self.Tb); Tmaxs.append(self.Tc)
            # Chosen as the model is weird
        if all([self.Tc, self.Pc, self.omega]):
            methods.append(NICOLA)
        if all([self.Tb, self.Tc]):
            methods.append(SATO_RIEDEL)
        if all([self.Hfus, self.Tc, self.omega]):
            methods.append(NICOLA_ORIGINAL)
        if all([self.Tc, self.Pc]):
            methods_P.extend([DIPPR_9G, MISSENARD])
        self.all_methods = set(methods)
        self.all_methods_P = set(methods_P)
        if Tmins and Tmaxs:
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)