def dPsat_dT(self, T):
        r'''Generic method to calculate the temperature derivative of vapor 
        pressure for a specified `T`. Implements the analytical derivative
        of the two polynomials described in `Psat`.
        
        As with `Psat`, results above the critical temperature are meaningless. 
        The first-order polynomial which is used to calculate it under 0.32 Tc
        may not be physicall meaningful, due to there normally not being a 
        volume solution to the EOS which can produce that low of a pressure.
        
        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        dPsat_dT : float
            Derivative of vapor pressure with respect to temperature, [Pa/K]
            
        Notes
        -----
        There is a small step change at 0.32 Tc for all EOS due to the two
        switch between polynomials at that point.
        
        Useful for calculating enthalpy of vaporization with the Clausius
        Clapeyron Equation. Derived with SymPy's diff and cse.
        '''
        a_alphas = self.a_alpha_and_derivatives(T)
        alpha, d_alpha_dT = a_alphas[0]/self.a, a_alphas[1]/self.a
        Tr = T/self.Tc
        if Tr >= 0.32:
            c = self.Psat_coeffs
            x0 = alpha/T
            x1 = -self.Tc*x0 + 1
            x2 = c[0]*x1
            x3 = c[2] - x1*(c[1] - x2)
            x4 = c[3] - x1*x3
            x5 = c[4] - x1*x4
            x6 = c[5] - x1*x5
            x7 = c[6] - x1*x6
            x8 = c[7] - x1*x7
            x9 = c[8] - x1*x8
            return self.Pc*(-(d_alpha_dT - x0)*(-c[9] + x1*x9 + x1*(-x1*(-x1*(-x1*(-x1*(-x1*(-x1*(-x1*(c[1] - 2*x2) + x3) + x4) + x5) + x6) + x7) + x8) + x9)) + 1./self.Tc)*exp(c[10] - x1*(c[9] - x1*(c[8] - x1*(c[7] - x1*(c[6] - x1*(c[5] - x1*(c[4] - x1*(c[3] - x1*(c[2] + x1*(-c[1] + x2))))))))))    
        else:
            c = self.Psat_coeffs_limiting
            return self.Pc*T*c[0]*(self.Tc*d_alpha_dT/T - self.Tc*alpha/(T*T))*exp(c[0]*(-1. + self.Tc*alpha/T) + c[1])/self.Tc + self.Pc*exp(c[0]*(-1. + self.Tc*alpha/T) + c[1])/self.Tc