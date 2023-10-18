def calculate(self, T, method):
        r'''Method to calculate a property with a specified method, with no
        validity checking or error handling. Demo function for testing only;
        must be implemented according to the methods available for each
        individual method. Include the interpolation call here.

        Parameters
        ----------
        T : float
            Temperature at which to calculate the property, [K]
        method : str
            Method name to use

        Returns
        -------
        prop : float
            Calculated property, [`units`]
        '''
        if method == TEST_METHOD_1:
            prop = self.TEST_METHOD_1_coeffs[0] + self.TEST_METHOD_1_coeffs[1]*T
        elif method == TEST_METHOD_2:
            prop = self.TEST_METHOD_2_coeffs[0] + self.TEST_METHOD_2_coeffs[1]*T
        elif method in self.tabular_data:
            prop = self.interpolate(T, method)
        return prop