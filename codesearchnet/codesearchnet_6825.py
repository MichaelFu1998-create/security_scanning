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
        if self.CASRN in CRC_inorg_s_const_data.index:
            methods.append(CRC_INORG_S)
            self.CRC_INORG_S_Vm = float(CRC_inorg_s_const_data.at[self.CASRN, 'Vm'])
#        if all((self.Tt, self.Vml_Tt, self.MW)):
#            self.rhol_Tt = Vm_to_rho(self.Vml_Tt, self.MW)
#            methods.append(GOODMAN)
        self.all_methods = set(methods)