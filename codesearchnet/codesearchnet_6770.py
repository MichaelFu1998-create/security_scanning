def a_alpha_and_derivatives(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives for this EOS. Returns `a_alpha`, `da_alpha_dT`, and 
        `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Uses the set values of `Tc`, `kappa`, and `a`. 
        
        For use in `solve_T`, returns only `a_alpha` if full is False.

        .. math::
            a\alpha = a \left(\kappa \left(- \frac{T^{0.5}}{Tc^{0.5}} 
            + 1\right) + 1\right)^{2}
        
            \frac{d a\alpha}{dT} = - \frac{1.0 a \kappa}{T^{0.5} Tc^{0.5}}
            \left(\kappa \left(- \frac{T^{0.5}}{Tc^{0.5}} + 1\right) + 1\right)

            \frac{d^2 a\alpha}{dT^2} = 0.5 a \kappa \left(- \frac{1}{T^{1.5} 
            Tc^{0.5}} \left(\kappa \left(\frac{T^{0.5}}{Tc^{0.5}} - 1\right)
            - 1\right) + \frac{\kappa}{T^{1.0} Tc^{1.0}}\right)
        '''
        if not full:
            return self.a*(1 + self.kappa*(1-(T/self.Tc)**0.5))**2
        else:
            if quick:
                Tc, kappa = self.Tc, self.kappa
                x0 = T**0.5
                x1 = Tc**-0.5
                x2 = kappa*(x0*x1 - 1.) - 1.
                x3 = self.a*kappa
                
                a_alpha = self.a*x2*x2
                da_alpha_dT = x1*x2*x3/x0
                d2a_alpha_dT2 = x3*(-0.5*T**-1.5*x1*x2 + 0.5/(T*Tc)*kappa)
            else:
                a_alpha = self.a*(1 + self.kappa*(1-(T/self.Tc)**0.5))**2
                da_alpha_dT = -self.a*self.kappa*sqrt(T/self.Tc)*(self.kappa*(-sqrt(T/self.Tc) + 1.) + 1.)/T
                d2a_alpha_dT2 = self.a*self.kappa*(self.kappa/self.Tc - sqrt(T/self.Tc)*(self.kappa*(sqrt(T/self.Tc) - 1.) - 1.)/T)/(2.*T)
            return a_alpha, da_alpha_dT, d2a_alpha_dT2