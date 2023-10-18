def Chen_Yang(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Hamid and Yang (2017) [1]_. Returns `a_alpha`,
        `da_alpha_dT`, and `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives`
        for more documentation. Seven coefficients needed.
        
        .. math::
            \alpha = e^{\left(- c_{3}^{\log{\left (\frac{T}{Tc} \right )}} 
            + 1\right) \left(- \frac{T c_{2}}{Tc} + c_{1}\right)}

        References
        ----------
        .. [1] Chen, Zehua, and Daoyong Yang. "Optimization of the Reduced 
           Temperature Associated with Peng–Robinson Equation of State and 
           Soave-Redlich-Kwong Equation of State To Improve Vapor Pressure 
           Prediction for Heavy Hydrocarbon Compounds." Journal of Chemical & 
           Engineering Data, August 31, 2017. doi:10.1021/acs.jced.7b00496.
        '''
        c1, c2, c3, c4, c5, c6, c7 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*exp(c4*log((-sqrt(T/Tc) + 1)*(c5 + c6*omega + c7*omega**2) + 1)**2 + (-T/Tc + 1)*(c1 + c2*omega + c3*omega**2))
        if not full:
            return a_alpha
        else:
            da_alpha_dT = a*(-(c1 + c2*omega + c3*omega**2)/Tc - c4*sqrt(T/Tc)*(c5 + c6*omega + c7*omega**2)*log((-sqrt(T/Tc) + 1)*(c5 + c6*omega + c7*omega**2) + 1)/(T*((-sqrt(T/Tc) + 1)*(c5 + c6*omega + c7*omega**2) + 1)))*exp(c4*log((-sqrt(T/Tc) + 1)*(c5 + c6*omega + c7*omega**2) + 1)**2 + (-T/Tc + 1)*(c1 + c2*omega + c3*omega**2))
            d2a_alpha_dT2 = a*(((c1 + c2*omega + c3*omega**2)/Tc - c4*sqrt(T/Tc)*(c5 + c6*omega + c7*omega**2)*log(-(sqrt(T/Tc) - 1)*(c5 + c6*omega + c7*omega**2) + 1)/(T*((sqrt(T/Tc) - 1)*(c5 + c6*omega + c7*omega**2) - 1)))**2 - c4*(c5 + c6*omega + c7*omega**2)*((c5 + c6*omega + c7*omega**2)*log(-(sqrt(T/Tc) - 1)*(c5 + c6*omega + c7*omega**2) + 1)/(Tc*((sqrt(T/Tc) - 1)*(c5 + c6*omega + c7*omega**2) - 1)) - (c5 + c6*omega + c7*omega**2)/(Tc*((sqrt(T/Tc) - 1)*(c5 + c6*omega + c7*omega**2) - 1)) + sqrt(T/Tc)*log(-(sqrt(T/Tc) - 1)*(c5 + c6*omega + c7*omega**2) + 1)/T)/(2*T*((sqrt(T/Tc) - 1)*(c5 + c6*omega + c7*omega**2) - 1)))*exp(c4*log(-(sqrt(T/Tc) - 1)*(c5 + c6*omega + c7*omega**2) + 1)**2 - (T/Tc - 1)*(c1 + c2*omega + c3*omega**2))
            return a_alpha, da_alpha_dT, d2a_alpha_dT2