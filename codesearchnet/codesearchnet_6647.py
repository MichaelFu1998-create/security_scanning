def calculate(self, T):
        r'''Method to actually calculate heat capacity as a function of 
        temperature.
            
        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        Cp : float
            Liquid heat capacity as T, [J/mol/K]
        '''        
        return Zabransky_cubic(T, *self.coeff_sets[self._coeff_ind_from_T(T)])