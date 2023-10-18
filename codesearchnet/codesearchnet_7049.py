def TP_dependent_property_derivative_T(self, T, P, order=1):
        r'''Method to calculate a derivative of a temperature and pressure
        dependent property with respect to temperature at constant pressure,
        of a given order. Methods found valid by `select_valid_methods_P` are 
        attempted until a method succeeds. If no methods are valid and succeed,
        None is returned.

        Calls `calculate_derivative_T` internally to perform the actual
        calculation.
        
        .. math::
            \text{derivative} = \frac{d (\text{property})}{d T}|_{P}

        Parameters
        ----------
        T : float
            Temperature at which to calculate the derivative, [K]
        P : float
            Pressure at which to calculate the derivative, [Pa]
        order : int
            Order of the derivative, >= 1

        Returns
        -------
        d_prop_d_T_at_P : float
            Calculated derivative property, [`units/K^order`]
        '''
        sorted_valid_methods_P = self.select_valid_methods_P(T, P)
        for method in sorted_valid_methods_P:
            try:
                return self.calculate_derivative_T(T, P, method, order)
            except:
                pass
        return None