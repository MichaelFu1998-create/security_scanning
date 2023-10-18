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
        if method == PERRY151:
            H2 = (self.PERRY151_const*T2 + 0.5*self.PERRY151_lin*T2**2 
                  - self.PERRY151_quadinv/T2 + self.PERRY151_quad*T2**3/3.)
            H1 = (self.PERRY151_const*T1 + 0.5*self.PERRY151_lin*T1**2 
                  - self.PERRY151_quadinv/T1 + self.PERRY151_quad*T1**3/3.)
            return (H2-H1)*calorie
        elif method == CRCSTD:
            return (T2-T1)*self.CRCSTD_Cp
        elif method == LASTOVKA_S:
            dH = (Lastovka_solid_integral(T2, self.similarity_variable)
                    - Lastovka_solid_integral(T1, self.similarity_variable))
            return property_mass_to_molar(dH, self.MW)
        elif method in self.tabular_data:
            return float(quad(self.calculate, T1, T2, args=(method))[0])
        else:
            raise Exception('Method not valid')