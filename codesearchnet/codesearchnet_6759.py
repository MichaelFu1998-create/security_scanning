def V_g_sat(self, T):
        r'''Method to calculate molar volume of the vapor phase along the
        saturation line.
        
        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        V_g_sat : float
            Gas molar volume along the saturation line, [m^3/mol]
            
        Notes
        -----
        Computers `Psat`, and then uses `volume_solutions` to obtain the three
        possible molar volumes. The highest value is returned.
        '''
        Psat = self.Psat(T)
        a_alpha = self.a_alpha_and_derivatives(T, full=False)
        Vs = self.volume_solutions(T, Psat, self.b, self.delta, self.epsilon, a_alpha)
        # Assume we can safely take the Vmax as gas, Vmin as l on the saturation line
        return max([i.real for i in Vs])