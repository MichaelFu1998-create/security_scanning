def fugacity_coefficients(self, Z, zs):
        r'''Literature formula for calculating fugacity coefficients for each
        species in a mixture. Verified numerically. Applicable to most 
        derivatives of the SRK equation of state as well.
        Called by `fugacities` on initialization, or by a solver routine 
        which is performing a flash calculation.
        
        .. math::
            \ln \hat \phi_i = \frac{B_i}{B}(Z-1) - \ln(Z-B) + \frac{A}{B}
            \left[\frac{B_i}{B} - \frac{2}{a \alpha}\sum_i y_i(a\alpha)_{ij}
            \right]\ln\left(1+\frac{B}{Z}\right)
            
            A=\frac{a\alpha P}{R^2T^2}
            
            B = \frac{bP}{RT}
        
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
        .. [1] Soave, Giorgio. "Equilibrium Constants from a Modified 
           Redlich-Kwong Equation of State." Chemical Engineering Science 27,
           no. 6 (June 1972): 1197-1203. doi:10.1016/0009-2509(72)80096-4.
        .. [2] Walas, Stanley M. Phase Equilibria in Chemical Engineering. 
           Butterworth-Heinemann, 1985.
        '''
        A = self.a_alpha*self.P/R2/self.T**2
        B = self.b*self.P/R/self.T
        phis = []
        for i in self.cmps:
            Bi = self.bs[i]*self.P/R/self.T
            t1 = Bi/B*(Z-1) - log(Z - B)
            t2 = A/B*(Bi/B - 2./self.a_alpha*sum([zs[j]*self.a_alpha_ijs[i][j] for j in self.cmps]))
            t3 = log(1. + B/Z)
            t4 = t1 + t2*t3
            phis.append(exp(t4))
        return phis