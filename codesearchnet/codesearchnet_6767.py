def Almeida(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Almeida et al. (1991) [1]_. Returns `a_alpha`, 
        `da_alpha_dT`, and `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives`  
        for more documentation. Three coefficients needed.
        
        .. math::
            \alpha = e^{c_{1} \left(- \frac{T}{Tc} + 1\right) \left|{
            \frac{T}{Tc} - 1}\right|^{c_{2} - 1} + c_{3} \left(-1 
            + \frac{Tc}{T}\right)}

        References
        ----------
        .. [1] Almeida, G. S., M. Aznar, and A. S. Telles. "Uma Nova Forma de 
           Dependência Com a Temperatura Do Termo Atrativo de Equações de 
           Estado Cúbicas." RBE, Rev. Bras. Eng., Cad. Eng. Quim 8 (1991): 95.
        '''
        # Note: For the second derivative, requires the use a CAS which can 
        # handle the assumption that Tr-1 != 0.
        c1, c2, c3 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*exp(c1*(-T/Tc + 1)*abs(T/Tc - 1)**(c2 - 1) + c3*(-1 + Tc/T))
        if not full:
            return a_alpha
        else:
            da_alpha_dT = a*((c1*(c2 - 1)*(-T/Tc + 1)*abs(T/Tc - 1)**(c2 - 1)*copysign(1, T/Tc - 1)/(Tc*Abs(T/Tc - 1)) - c1*abs(T/Tc - 1)**(c2 - 1)/Tc - Tc*c3/T**2)*exp(c1*(-T/Tc + 1)*abs(T/Tc - 1)**(c2 - 1) + c3*(-1 + Tc/T)))
            d2a_alpha_dT2 = a*exp(c3*(Tc/T - 1) - c1*abs(T/Tc - 1)**(c2 - 1)*(T/Tc - 1))*((c1*abs(T/Tc - 1)**(c2 - 1))/Tc + (Tc*c3)/T**2 + (c1*abs(T/Tc - 1)**(c2 - 2)*copysign(1, T/Tc - 1)*(c2 - 1)*(T/Tc - 1))/Tc)**2 - exp(c3*(Tc/T - 1) - c1*abs(T/Tc - 1)**(c2 - 1)*(T/Tc - 1))*((2*c1*abs(T/Tc - 1)**(c2 - 2)*copysign(1, T/Tc - 1)*(c2 - 1))/Tc**2 - (2*Tc*c3)/T**3 + (c1*abs(T/Tc - 1)**(c2 - 3)*copysign(1, T/Tc - 1)**2*(c2 - 1)*(c2 - 2)*(T/Tc - 1))/Tc**2)
            return a_alpha, da_alpha_dT, d2a_alpha_dT2