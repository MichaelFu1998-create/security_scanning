def property_derivative_P(self, T, P, zs, ws, order=1):
        r'''Method to calculate a derivative of a mixture property with respect
        to pressure at constant temperature and composition,
        of a given order. Methods found valid by `select_valid_methods` are 
        attempted until a method succeeds. If no methods are valid and succeed,
        None is returned.

        Calls `calculate_derivative_P` internally to perform the actual
        calculation.
        
        .. math::
            \text{derivative} = \frac{d (\text{property})}{d P}|_{T, z}

        Parameters
        ----------
        T : float
            Temperature at which to calculate the derivative, [K]
        P : float
            Pressure at which to calculate the derivative, [Pa]
        zs : list[float]
            Mole fractions of all species in the mixture, [-]
        ws : list[float]
            Weight fractions of all species in the mixture, [-]
        order : int
            Order of the derivative, >= 1

        Returns
        -------
        d_prop_d_P_at_T : float
            Calculated derivative property, [`units/Pa^order`]
        '''
        sorted_valid_methods = self.select_valid_methods(T, P, zs, ws)
        for method in sorted_valid_methods:
            try:
                return self.calculate_derivative_P(P, T, zs, ws, method, order)
            except:
                pass
        return None