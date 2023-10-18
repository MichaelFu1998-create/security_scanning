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
        methods = [DIPPR_9H, SIMPLE]        
        if len(self.CASs) == 2:
            methods.append(FILIPPOV)
        if '7732-18-5' in self.CASs and len(self.CASs)>1:
            wCASs = [i for i in self.CASs if i != '7732-18-5']
            if all([i in Magomedovk_thermal_cond.index for i in wCASs]):
                methods.append(MAGOMEDOV)
                self.wCASs = wCASs
                self.index_w = self.CASs.index('7732-18-5')
            
        self.all_methods = set(methods)
        Tmins = [i.Tmin for i in self.ThermalConductivityLiquids if i.Tmin]
        Tmaxs = [i.Tmax for i in self.ThermalConductivityLiquids if i.Tmax]
        if Tmins:
            self.Tmin = max(Tmins)
        if Tmaxs:
            self.Tmax = max(Tmaxs)