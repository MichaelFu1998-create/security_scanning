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
        if self.CASRN and self.CASRN in _PerryI and 'c' in _PerryI[self.CASRN]:
            self.PERRY151_Tmin = _PerryI[self.CASRN]['c']['Tmin'] if _PerryI[self.CASRN]['c']['Tmin'] else 0
            self.PERRY151_Tmax = _PerryI[self.CASRN]['c']['Tmax'] if _PerryI[self.CASRN]['c']['Tmax'] else 2000
            self.PERRY151_const = _PerryI[self.CASRN]['c']['Const']
            self.PERRY151_lin = _PerryI[self.CASRN]['c']['Lin']
            self.PERRY151_quad = _PerryI[self.CASRN]['c']['Quad']
            self.PERRY151_quadinv = _PerryI[self.CASRN]['c']['Quadinv']
            methods.append(PERRY151)
            Tmins.append(self.PERRY151_Tmin); Tmaxs.append(self.PERRY151_Tmax)
        if self.CASRN in CRC_standard_data.index and not np.isnan(CRC_standard_data.at[self.CASRN, 'Cpc']):
            self.CRCSTD_Cp = float(CRC_standard_data.at[self.CASRN, 'Cpc'])
            methods.append(CRCSTD)
        if self.MW and self.similarity_variable:
            methods.append(LASTOVKA_S)
            Tmins.append(1.0); Tmaxs.append(10000)
            # Works above roughly 1 K up to 10K.
        self.all_methods = set(methods)
        if Tmins and Tmaxs:
            self.Tmin, self.Tmax = min(Tmins), max(Tmaxs)