def T_dependent_property(self, T):
        r'''Method to calculate the property with sanity checking and without
        specifying a specific method. `select_valid_methods` is used to obtain
        a sorted list of methods to try. Methods are then tried in order until
        one succeeds. The methods are allowed to fail, and their results are
        checked with `test_property_validity`. On success, the used method
        is stored in the variable `method`.

        If `method` is set, this method is first checked for validity with
        `test_method_validity` for the specified temperature, and if it is
        valid, it is then used to calculate the property. The result is checked
        for validity, and returned if it is valid. If either of the checks fail,
        the function retrieves a full list of valid methods with
        `select_valid_methods` and attempts them as described above.

        If no methods are found which succeed, returns None.

        Parameters
        ----------
        T : float
            Temperature at which to calculate the property, [K]

        Returns
        -------
        prop : float
            Calculated property, [`units`]
        '''
        # Optimistic track, with the already set method
        if self.method:
            # retest within range
            if self.test_method_validity(T, self.method):
                try:
                    prop = self.calculate(T, self.method)
                    if self.test_property_validity(prop):
                        return prop
                except:  # pragma: no cover
                    pass

        # get valid methods at T, and try them until one yields a valid
        # property; store the method and return the answer
        self.sorted_valid_methods = self.select_valid_methods(T)
        for method in self.sorted_valid_methods:
            try:
                prop = self.calculate(T, method)
                if self.test_property_validity(prop):
                    self.method = method
                    return prop
            except:  # pragma: no cover
                pass

        # Function returns None if it does not work.
        return None