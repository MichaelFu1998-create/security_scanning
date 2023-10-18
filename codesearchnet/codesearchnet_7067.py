def fugacity_coefficients(self, Z, zs):
        r'''Literature formula for calculating fugacity coefficients for each
        species in a mixture. Verified numerically.
        Called by `fugacities` on initialization, or by a solver routine 
        which is performing a flash calculation.
        
        .. math::
            \ln \hat \phi_i = \frac{b_i}{V-b} - \ln\left[Z\left(1
            - \frac{b}{V}\right)\right] - \frac{2\sqrt{aa_i}}{RTV}
        
        Parameters
        ----------
        Z : float
            Compressibility of the mixture for a desired phase, [-]
        zs : list[float], optional
            List of mole factions, either overall or in a specific phase, [-]
        
        Returns
        -------
        phis : float
            Fugacity coefficient for each species, [-]
                         
        References
        ----------
        .. [1] Walas, Stanley M. Phase Equilibria in Chemical Engineering. 
           Butterworth-Heinemann, 1985.
        '''
        phis = []
        V = Z*R*self.T/self.P
        for i in self.cmps:
            phi = self.bs[i]/(V-self.b) - log(Z*(1. - self.b/V)) - 2.*(self.a_alpha*self.ais[i])**0.5/(R*self.T*V)
            phis.append(exp(phi))
        return phis