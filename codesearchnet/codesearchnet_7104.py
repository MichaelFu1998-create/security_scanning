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
        methods = []        
        methods.append(SIMPLE)
        if none_and_length_check((self.Tbs, self.MWs)):
            methods.append(LINDSAY_BROMLEY)
        self.all_methods = set(methods)
        Tmins = [i.Tmin for i in self.ThermalConductivityGases if i.Tmin]
        Tmaxs = [i.Tmax for i in self.ThermalConductivityGases if i.Tmax]
        if Tmins:
            self.Tmin = max(Tmins)
        if Tmaxs:
            self.Tmax = max(Tmaxs)