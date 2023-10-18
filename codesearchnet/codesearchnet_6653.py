def calculate_integral_over_T(self, T1, T2, method):
        r'''Method to calculate the integral of a property over temperature
        with respect to temperature, using a specified method.   Implements the 
        analytical integrals of all available methods except for tabular data,
        the case of multiple coefficient sets needed to encompass the temperature
        range of any of the ZABRANSKY methods, and the CSP methods using the
        vapor phase properties.

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
        if method == ZABRANSKY_SPLINE:
            return self.Zabransky_spline.calculate_integral_over_T(T1, T2)
        elif method == ZABRANSKY_SPLINE_C:
            return self.Zabransky_spline_iso.calculate_integral_over_T(T1, T2)
        elif method == ZABRANSKY_SPLINE_SAT:
            return self.Zabransky_spline_sat.calculate_integral_over_T(T1, T2)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL:
            return self.Zabransky_quasipolynomial.calculate_integral_over_T(T1, T2)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL_C:
            return self.Zabransky_quasipolynomial_iso.calculate_integral_over_T(T1, T2)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL_SAT:
            return self.Zabransky_quasipolynomial_sat.calculate_integral_over_T(T1, T2)
        elif method == POLING_CONST:
            return self.POLING_constant*log(T2/T1)
        elif method == CRCSTD:
            return self.CRCSTD_constant*log(T2/T1)
        elif method == DADGOSTAR_SHAW:
            dS = (Dadgostar_Shaw_integral_over_T(T2, self.similarity_variable)
                    - Dadgostar_Shaw_integral_over_T(T1, self.similarity_variable))
            return property_mass_to_molar(dS, self.MW)
        elif method in self.tabular_data or method == COOLPROP or method in [ROWLINSON_POLING, ROWLINSON_BONDI]:
            return float(quad(lambda T: self.calculate(T, method)/T, T1, T2)[0])
        else:
            raise Exception('Method not valid')