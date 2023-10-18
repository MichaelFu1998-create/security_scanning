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
        if self.CASRN in CRC_Permittivity_data.index:
            methods.append(CRC_CONSTANT)
            _, self.CRC_CONSTANT_T, self.CRC_permittivity, A, B, C, D, Tmin, Tmax = _CRC_Permittivity_data_values[CRC_Permittivity_data.index.get_loc(self.CASRN)].tolist()
            self.CRC_Tmin = Tmin
            self.CRC_Tmax = Tmax
            self.CRC_coeffs = [0 if np.isnan(x) else x for x in [A, B, C, D] ]
            if not np.isnan(Tmin):
                Tmins.append(Tmin); Tmaxs.append(Tmax)
            if self.CRC_coeffs[0]:
                methods.append(CRC)
        self.all_methods = set(methods)
        if Tmins and Tmaxs:
            self.Tmin = min(Tmins)
            self.Tmax = max(Tmaxs)