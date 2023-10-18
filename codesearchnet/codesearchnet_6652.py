def calculate_integral(self, T1, T2, method):
        r'''Method to calculate the integral of a property with respect to
        temperature, using a specified method.  Implements the 
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
            [`units*K`]
        '''
        if method == ZABRANSKY_SPLINE:
            return self.Zabransky_spline.calculate_integral(T1, T2)
        elif method == ZABRANSKY_SPLINE_C:
            return self.Zabransky_spline_iso.calculate_integral(T1, T2)
        elif method == ZABRANSKY_SPLINE_SAT:
            return self.Zabransky_spline_sat.calculate_integral(T1, T2)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL:
            return self.Zabransky_quasipolynomial.calculate_integral(T1, T2)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL_C:
            return self.Zabransky_quasipolynomial_iso.calculate_integral(T1, T2)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL_SAT:
            return self.Zabransky_quasipolynomial_sat.calculate_integral(T1, T2)
        elif method == POLING_CONST:
            return (T2 - T1)*self.POLING_constant
        elif method == CRCSTD:
            return (T2 - T1)*self.CRCSTD_constant
        elif method == DADGOSTAR_SHAW:
            dH = (Dadgostar_Shaw_integral(T2, self.similarity_variable)
                    - Dadgostar_Shaw_integral(T1, self.similarity_variable))
            return property_mass_to_molar(dH, self.MW)
        elif method in self.tabular_data or method == COOLPROP or method in [ROWLINSON_POLING, ROWLINSON_BONDI]:
            return float(quad(self.calculate, T1, T2, args=(method))[0])
        else:
            raise Exception('Method not valid')