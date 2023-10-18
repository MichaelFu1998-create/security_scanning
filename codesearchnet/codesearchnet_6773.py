def a_alpha_and_derivatives(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives for this EOS. Returns `a_alpha`, `da_alpha_dT`, and 
        `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Uses the set values of `Tc`, `kappa0`, `kappa1`, and 
        `a`. 
        
        For use in root-finding, returns only `a_alpha` if full is False.

        The `a_alpha` function is shown below; its first and second derivatives
        are long available through the SymPy expression under it.

        .. math::
            a\alpha = a \left(\left(\kappa_{0} + \kappa_{1} \left(\sqrt{\frac{
            T}{Tc}} + 1\right) \left(- \frac{T}{Tc} + \frac{7}{10}\right)
            \right) \left(- \sqrt{\frac{T}{Tc}} + 1\right) + 1\right)^{2}
            
        >>> from sympy import *
        >>> P, T, V = symbols('P, T, V')
        >>> Tc, Pc, omega = symbols('Tc, Pc, omega')
        >>> R, a, b, kappa0, kappa1 = symbols('R, a, b, kappa0, kappa1')
        >>> kappa = kappa0 + kappa1*(1 + sqrt(T/Tc))*(Rational(7, 10)-T/Tc)
        >>> a_alpha = a*(1 + kappa*(1-sqrt(T/Tc)))**2
        >>> # diff(a_alpha, T)
        >>> # diff(a_alpha, T, 2)
        '''
        Tc, a, kappa0, kappa1 = self.Tc, self.a, self.kappa0, self.kappa1
        if not full:
            return a*((kappa0 + kappa1*(sqrt(T/Tc) + 1)*(-T/Tc + 0.7))*(-sqrt(T/Tc) + 1) + 1)**2
        else:
            if quick:
                x1 = T/Tc
                x2 = x1**0.5
                x3 = x2 - 1.
                x4 = 10.*x1 - 7.
                x5 = x2 + 1.
                x6 = 10.*kappa0 - kappa1*x4*x5
                x7 = x3*x6
                x8 = x7*0.1 - 1.
                x10 = x6/T
                x11 = kappa1*x3
                x12 = x4/T
                x13 = 20./Tc*x5 + x12*x2
                x14 = -x10*x2 + x11*x13
                a_alpha = a*x8*x8
                da_alpha_dT = -a*x14*x8*0.1
                d2a_alpha_dT2 = a*(x14*x14 - x2/T*(x7 - 10.)*(2.*kappa1*x13 + x10 + x11*(40./Tc - x12)))/200.
            else:
                a_alpha = a*((kappa0 + kappa1*(sqrt(T/Tc) + 1)*(-T/Tc + 0.7))*(-sqrt(T/Tc) + 1) + 1)**2
                da_alpha_dT = a*((kappa0 + kappa1*(sqrt(T/Tc) + 1)*(-T/Tc + 0.7))*(-sqrt(T/Tc) + 1) + 1)*(2*(-sqrt(T/Tc) + 1)*(-kappa1*(sqrt(T/Tc) + 1)/Tc + kappa1*sqrt(T/Tc)*(-T/Tc + 0.7)/(2*T)) - sqrt(T/Tc)*(kappa0 + kappa1*(sqrt(T/Tc) + 1)*(-T/Tc + 0.7))/T)
                d2a_alpha_dT2 = a*((kappa1*(sqrt(T/Tc) - 1)*(20*(sqrt(T/Tc) + 1)/Tc + sqrt(T/Tc)*(10*T/Tc - 7)/T) - sqrt(T/Tc)*(10*kappa0 - kappa1*(sqrt(T/Tc) + 1)*(10*T/Tc - 7))/T)**2 - sqrt(T/Tc)*((10*kappa0 - kappa1*(sqrt(T/Tc) + 1)*(10*T/Tc - 7))*(sqrt(T/Tc) - 1) - 10)*(kappa1*(40/Tc - (10*T/Tc - 7)/T)*(sqrt(T/Tc) - 1) + 2*kappa1*(20*(sqrt(T/Tc) + 1)/Tc + sqrt(T/Tc)*(10*T/Tc - 7)/T) + (10*kappa0 - kappa1*(sqrt(T/Tc) + 1)*(10*T/Tc - 7))/T)/T)/200
            return a_alpha, da_alpha_dT, d2a_alpha_dT2