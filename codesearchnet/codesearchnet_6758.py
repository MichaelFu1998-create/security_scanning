def V_l_sat(self, T):
        r'''Method to calculate molar volume of the liquid phase along the
        saturation line.
        
        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        V_l_sat : float
            Liquid molar volume along the saturation line, [m^3/mol]
            
        Notes
        -----
        Computers `Psat`, and then uses `volume_solutions` to obtain the three
        possible molar volumes. The lowest value is returned.
        '''
        Psat = self.Psat(T)
        a_alpha = self.a_alpha_and_derivatives(T, full=False)
        Vs = self.volume_solutions(T, Psat, self.b, self.delta, self.epsilon, a_alpha)
        # Assume we can safely take the Vmax as gas, Vmin as l on the saturation line
        return min([i.real for i in Vs])