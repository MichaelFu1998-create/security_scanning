def load_all_methods(self):
        r'''Method to initialize the object by precomputing any values which
        may be used repeatedly and by retrieving mixture-specific variables.
        All data are stored as attributes. This method also sets :obj:`Tmin`, 
        :obj:`Tmax`, and :obj:`all_methods` as a set of methods which should 
        work to calculate the property.

        Called on initialization only. See the source code for the variables at
        which the coefficients are stored. The coefficients can safely be
        altered once the class is initialized. This method can be called again
        to reset the parameters.
        '''
        methods = [SIMPLE]        
        
        if none_and_length_check([self.Tcs, self.Vcs, self.omegas, self.CASs]):
            methods.append(COSTALD_MIXTURE)
            if all([i in COSTALD_data.index for i in self.CASs]):
                self.COSTALD_Vchars = [COSTALD_data.at[CAS, 'Vchar'] for CAS in self.CASs]
                self.COSTALD_omegas = [COSTALD_data.at[CAS, 'omega_SRK'] for CAS in self.CASs]
                methods.append(COSTALD_MIXTURE_FIT)
            
        if none_and_length_check([self.MWs, self.Tcs, self.Pcs, self.Zcs, self.CASs]):
            methods.append(RACKETT)
            if all([CAS in COSTALD_data.index for CAS in self.CASs]):
                Z_RAs = [COSTALD_data.at[CAS, 'Z_RA'] for CAS in self.CASs]
                if not any(np.isnan(Z_RAs)):
                    self.Z_RAs = Z_RAs
                    methods.append(RACKETT_PARAMETERS)
        
        if len(self.CASs) > 1 and '7732-18-5' in self.CASs:
            wCASs = [i for i in self.CASs if i != '7732-18-5'] 
            if all([i in _Laliberte_Density_ParametersDict for i in wCASs]):
                methods.append(LALIBERTE)
                self.wCASs = wCASs
                self.index_w = self.CASs.index('7732-18-5')
        self.all_methods = set(methods)