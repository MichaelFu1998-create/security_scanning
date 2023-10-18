def T_dependent_property_integral_over_T(self, T1, T2):
        r'''Method to calculate the integral of a property over temperature 
        with respect to temperature, using a specified method. Methods found
        valid by `select_valid_methods` are attempted until a method succeeds. 
        If no methods are valid and succeed, None is returned.
        
        Calls `calculate_integral_over_T` internally to perform the actual
        calculation.
        
        .. math::
            \text{integral} = \int_{T_1}^{T_2} \frac{\text{property}}{T} \; dT

        Parameters
        ----------
        T1 : float
            Lower limit of integration, [K]
        T2 : float
            Upper limit of integration, [K]
        method : str
            Method for which to find the integral

        Returns
        -------
        integral : float
            Calculated integral of the property over the given range, 
            [`units`]
        '''
        Tavg = 0.5*(T1+T2)
        if self.method:
            # retest within range
            if self.test_method_validity(Tavg, self.method):
                try:
                    return self.calculate_integral_over_T(T1, T2, self.method)
                except:  # pragma: no cover
                    pass
                
        sorted_valid_methods = self.select_valid_methods(Tavg)
        for method in sorted_valid_methods:
            try:
                return self.calculate_integral_over_T(T1, T2, method)
            except:
                pass
        return None