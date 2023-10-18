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
            Ts, props = VDI_tabular_data(self.CASRN, 'K (g)')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP); methods_P.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tmin); Tmaxs.append(self.CP_f.Tc)
        if self.CASRN in Perrys2_314.index:
            methods.append(DIPPR_PERRY_8E)
            _, C1, C2, C3, C4, self.Perrys2_314_Tmin, self.Perrys2_314_Tmax = _Perrys2_314_values[Perrys2_314.index.get_loc(self.CASRN)].tolist()
            self.Perrys2_314_coeffs = [C1, C2, C3, C4]
            Tmins.append(self.Perrys2_314_Tmin); Tmaxs.append(self.Perrys2_314_Tmax)
        if self.CASRN in VDI_PPDS_10.index:
            _,  A, B, C, D, E = _VDI_PPDS_10_values[VDI_PPDS_10.index.get_loc(self.CASRN)].tolist()
            self.VDI_PPDS_coeffs = [A, B, C, D, E]
            self.VDI_PPDS_coeffs.reverse()
            methods.append(VDI_PPDS)
        if all((self.MW, self.Tb, self.Pc, self.omega)):
            methods.append(GHARAGHEIZI_G)
            # Turns negative at low T; do not set Tmin
            Tmaxs.append(3000)
        if all((self.Cvgm, self.mug, self.MW, self.Tc)):
            methods.append(DIPPR_9B)
            Tmins.append(0.01); Tmaxs.append(1E4)  # No limit here
        if all((self.Cvgm, self.mug, self.MW, self.Tc, self.omega)):
            methods.append(CHUNG)
            Tmins.append(0.01); Tmaxs.append(1E4)  # No limit
        if all((self.Cvgm, self.MW, self.Tc, self.Vc, self.Zc, self.omega)):
            methods.append(ELI_HANLEY)
            Tmaxs.append(1E4)  # Numeric error at low T
        if all((self.Cvgm, self.mug, self.MW)):
            methods.append(EUCKEN_MOD)
            methods.append(EUCKEN)
            Tmins.append(0.01); Tmaxs.append(1E4)  # No limits
        if self.MW:
            methods.append(BAHADORI_G)
            # Terrible method, so don't set methods
        if all([self.MW, self.Tc, self.Vc, self.Zc, self.omega]):
            methods_P.append(ELI_HANLEY_DENSE)
        if all([self.MW, self.Tc, self.Vc, self.omega, self.dipole]):
            methods_P.append(CHUNG_DENSE)
        if all([self.MW, self.Tc, self.Pc, self.Vc, self.Zc]):
            methods_P.append(STIEL_THODOS_DENSE)
        self.all_methods = set(methods)
        self.all_methods_P = set(methods_P)
        if Tmins and Tmaxs:
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)