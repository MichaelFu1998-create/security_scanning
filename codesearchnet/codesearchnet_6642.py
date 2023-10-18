def calculate_integral_over_T(self, T1, T2, method):
        r'''Method to calculate the integral of a property over temperature
        with respect to temperature, using a specified method. Implements the 
        analytical integrals of all available methods except for tabular data.
        
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
        if method == TRCIG:
            S2 = TRCCp_integral_over_T(T2, *self.TRCIG_coefs)
            S1 = TRCCp_integral_over_T(T1, *self.TRCIG_coefs)
            return S2 - S1
        elif method == CRCSTD:
            return self.CRCSTD_constant*log(T2/T1)
        elif method == POLING_CONST:
            return self.POLING_constant*log(T2/T1)
        elif method == POLING:
            A, B, C, D, E = self.POLING_coefs
            S2 = ((((0.25*E)*T2 + D/3.)*T2 + 0.5*C)*T2 + B)*T2 
            S1 = ((((0.25*E)*T1 + D/3.)*T1 + 0.5*C)*T1 + B)*T1
            return R*(S2-S1 + A*log(T2/T1))
        elif method == LASTOVKA_SHAW:
            dS = (Lastovka_Shaw_integral_over_T(T2, self.similarity_variable)
                 - Lastovka_Shaw_integral_over_T(T1, self.similarity_variable))
            return property_mass_to_molar(dS, self.MW)
        elif method in self.tabular_data or method == COOLPROP:
            return float(quad(lambda T: self.calculate(T, method)/T, T1, T2)[0])
        else:
            raise Exception('Method not valid')