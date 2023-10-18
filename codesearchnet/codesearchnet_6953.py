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
            Ts, props = VDI_tabular_data(self.CASRN, 'Mu (g)')
            self.VDI_Tmin = Ts[0]
            self.VDI_Tmax = Ts[-1]
            self.tabular_data[VDI_TABULAR] = (Ts, props)
            Tmins.append(self.VDI_Tmin); Tmaxs.append(self.VDI_Tmax)
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods.append(COOLPROP); methods_P.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
            Tmins.append(self.CP_f.Tmin); Tmaxs.append(self.CP_f.Tmax)
        if self.CASRN in Perrys2_312.index:
            methods.append(DIPPR_PERRY_8E)
            _, C1, C2, C3, C4, self.Perrys2_312_Tmin, self.Perrys2_312_Tmax = _Perrys2_312_values[Perrys2_312.index.get_loc(self.CASRN)].tolist()
            self.Perrys2_312_coeffs = [C1, C2, C3, C4]
            Tmins.append(self.Perrys2_312_Tmin); Tmaxs.append(self.Perrys2_312_Tmax)
        if self.CASRN in VDI_PPDS_8.index:
            methods.append(VDI_PPDS)
            self.VDI_PPDS_coeffs = _VDI_PPDS_8_values[VDI_PPDS_8.index.get_loc(self.CASRN)].tolist()[1:]
            self.VDI_PPDS_coeffs.reverse() # in format for horner's scheme
        if all([self.Tc, self.Pc, self.MW]):
            methods.append(GHARAGHEIZI)
            methods.append(YOON_THODOS)
            methods.append(STIEL_THODOS)
            Tmins.append(0); Tmaxs.append(5E3)  # Intelligently set limit
            # GHARAGHEIZI turns nonsesical at ~15 K, YOON_THODOS fine to 0 K,
            # same as STIEL_THODOS
        if all([self.Tc, self.Pc, self.Zc, self.MW]):
            methods.append(LUCAS_GAS)
            Tmins.append(0); Tmaxs.append(1E3)
        self.all_methods = set(methods)
        self.all_methods_P = set(methods_P)
        if Tmins and Tmaxs:
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)