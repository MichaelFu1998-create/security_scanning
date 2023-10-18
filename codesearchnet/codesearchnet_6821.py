def load_all_methods(self):
        r'''Method which picks out coefficients for the specified chemical
        from the various dictionaries and DataFrames storing it. All data is
        stored as attributes. This method also sets obj:`all_methods_P` as a
        set of methods for which the data exists for.

        Called on initialization only. See the source code for the variables at
        which the coefficients are stored. The coefficients can safely be
        altered once the class is initialized. This method can be called again
        to reset the parameters.
        '''
        methods_P = [IDEAL]
        # no point in getting Tmin, Tmax
        if all((self.Tc, self.Pc, self.omega)):
            methods_P.extend([TSONOPOULOS_EXTENDED, TSONOPOULOS, ABBOTT,
                            PITZER_CURL])
            if self.eos:
                methods_P.append(EOS)
        if self.CASRN in CRC_virial_data.index:
            methods_P.append(CRC_VIRIAL)
            self.CRC_VIRIAL_coeffs = _CRC_virial_data_values[CRC_virial_data.index.get_loc(self.CASRN)].tolist()[1:]
        if has_CoolProp and self.CASRN in coolprop_dict:
            methods_P.append(COOLPROP)
            self.CP_f = coolprop_fluids[self.CASRN]
        self.all_methods_P = set(methods_P)