def calculate_integral(self, T1, T2, method):
        r'''Method to calculate the integral of a property with respect to
        temperature, using a specified method. Implements the analytical
        integrals of all available methods except for tabular data.
        
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
        if method == TRCIG:
            H2 = TRCCp_integral(T2, *self.TRCIG_coefs)
            H1 = TRCCp_integral(T1, *self.TRCIG_coefs)
            return H2 - H1
        elif method == POLING:
            A, B, C, D, E = self.POLING_coefs
            H2 = (((((0.2*E)*T2 + 0.25*D)*T2 + C/3.)*T2 + 0.5*B)*T2 + A)*T2
            H1 = (((((0.2*E)*T1 + 0.25*D)*T1 + C/3.)*T1 + 0.5*B)*T1 + A)*T1
            return R*(H2 - H1)
        elif method == POLING_CONST:
            return (T2 - T1)*self.POLING_constant
        elif method == CRCSTD:
            return (T2 - T1)*self.CRCSTD_constant
        elif method == LASTOVKA_SHAW:
            dH = (Lastovka_Shaw_integral(T2, self.similarity_variable)
                    - Lastovka_Shaw_integral(T1, self.similarity_variable))
            return property_mass_to_molar(dH, self.MW)
        elif method in self.tabular_data or method == COOLPROP:
            return float(quad(self.calculate, T1, T2, args=(method))[0])
        else:
            raise Exception('Method not valid')