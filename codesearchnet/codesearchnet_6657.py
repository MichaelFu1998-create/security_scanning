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
        if method == PERRY151:
            S2 = (self.PERRY151_const*log(T2) + self.PERRY151_lin*T2 
                  - self.PERRY151_quadinv/(2.*T2**2) + 0.5*self.PERRY151_quad*T2**2)
            S1 = (self.PERRY151_const*log(T1) + self.PERRY151_lin*T1
                  - self.PERRY151_quadinv/(2.*T1**2) + 0.5*self.PERRY151_quad*T1**2)
            return (S2 - S1)*calorie
        elif method == CRCSTD:
            S2 = self.CRCSTD_Cp*log(T2)
            S1 = self.CRCSTD_Cp*log(T1)
            return (S2 - S1)
        elif method == LASTOVKA_S:
            dS = (Lastovka_solid_integral_over_T(T2, self.similarity_variable)
                    - Lastovka_solid_integral_over_T(T1, self.similarity_variable))
            return property_mass_to_molar(dS, self.MW)
        elif method in self.tabular_data:
            return float(quad(lambda T: self.calculate(T, method)/T, T1, T2)[0])
        else:
            raise Exception('Method not valid')