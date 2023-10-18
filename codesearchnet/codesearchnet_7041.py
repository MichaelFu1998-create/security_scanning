def TP_dependent_property(self, T, P):
        r'''Method to calculate the property with sanity checking and without
        specifying a specific method. `select_valid_methods_P` is used to obtain
        a sorted list of methods to try. Methods are then tried in order until
        one succeeds. The methods are allowed to fail, and their results are
        checked with `test_property_validity`. On success, the used method
        is stored in the variable `method_P`.

        If `method_P` is set, this method is first checked for validity with
        `test_method_validity_P` for the specified temperature, and if it is
        valid, it is then used to calculate the property. The result is checked
        for validity, and returned if it is valid. If either of the checks fail,
        the function retrieves a full list of valid methods with
        `select_valid_methods_P` and attempts them as described above.

        If no methods are found which succeed, returns None.

        Parameters
        ----------
        T : float
            Temperature at which to calculate the property, [K]
        P : float
            Pressure at which to calculate the property, [Pa]

        Returns
        -------
        prop : float
            Calculated property, [`units`]
        '''
        # Optimistic track, with the already set method
        if self.method_P:
            # retest within range
            if self.test_method_validity_P(T, P, self.method_P):
                try:
                    prop = self.calculate_P(T, P, self.method_P)
                    if self.test_property_validity(prop):
                        return prop
                except:  # pragma: no cover
                    pass

        # get valid methods at T, and try them until one yields a valid
        # property; store the method_P and return the answer
        self.sorted_valid_methods_P = self.select_valid_methods_P(T, P)
        for method_P in self.sorted_valid_methods_P:
            try:
                prop = self.calculate_P(T, P, method_P)
                if self.test_property_validity(prop):
                    self.method_P = method_P
                    return prop
            except:  # pragma: no cover
                pass
        # Function returns None if it does not work.
        return None