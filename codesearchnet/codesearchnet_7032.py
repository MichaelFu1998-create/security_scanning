def T_dependent_property_derivative(self, T, order=1):
        r'''Method to obtain a derivative of a property with respect to 
        temperature, of a given order. Methods found valid by 
        `select_valid_methods` are attempted until a method succeeds. If no 
        methods are valid and succeed, None is returned.

        Calls `calculate_derivative` internally to perform the actual
        calculation.
        
        .. math::
            \text{derivative} = \frac{d (\text{property})}{d T}

        Parameters
        ----------
        T : float
            Temperature at which to calculate the derivative, [K]
        order : int
            Order of the derivative, >= 1

        Returns
        -------
        derivative : float
            Calculated derivative property, [`units/K^order`]
        '''
        if self.method:
            # retest within range
            if self.test_method_validity(T, self.method):
                try:
                    return self.calculate_derivative(T, self.method, order)
                except:  # pragma: no cover
                    pass
        sorted_valid_methods = self.select_valid_methods(T)
        for method in sorted_valid_methods:
            try:
                return self.calculate_derivative(T, method, order)
            except:
                pass
        return None