def a_alpha_and_derivatives(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives for this EOS. Returns `a_alpha`, `da_alpha_dT`, and 
        `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Uses the set values of `Tc`, `a`, `S1`, and `S2`. 
        
        .. math::
            a\alpha(T) = a\left[1 + S_1\left(1-\sqrt{T_r}\right) + S_2\frac{1
            - \sqrt{T_r}}{\sqrt{T_r}}\right]^2
        
            \frac{d a\alpha}{dT} = a\frac{Tc}{T^{2}} \left(- S_{2} \left(\sqrt{
            \frac{T}{Tc}} - 1\right) + \sqrt{\frac{T}{Tc}} \left(S_{1} \sqrt{
            \frac{T}{Tc}} + S_{2}\right)\right) \left(S_{2} \left(\sqrt{\frac{
            T}{Tc}} - 1\right) + \sqrt{\frac{T}{Tc}} \left(S_{1} \left(\sqrt{
            \frac{T}{Tc}} - 1\right) - 1\right)\right)

            \frac{d^2 a\alpha}{dT^2} = a\frac{1}{2 T^{3}} \left(S_{1}^{2} T
            \sqrt{\frac{T}{Tc}} - S_{1} S_{2} T \sqrt{\frac{T}{Tc}} + 3 S_{1}
            S_{2} Tc \sqrt{\frac{T}{Tc}} + S_{1} T \sqrt{\frac{T}{Tc}} 
            - 3 S_{2}^{2} Tc \sqrt{\frac{T}{Tc}} + 4 S_{2}^{2} Tc + 3 S_{2} 
            Tc \sqrt{\frac{T}{Tc}}\right)
        '''
        a, Tc, S1, S2 = self.a, self.Tc, self.S1, self.S2
        if not full:
            return a*(S1*(-(T/Tc)**0.5 + 1.) + S2*(-(T/Tc)**0.5 + 1)*(T/Tc)**-0.5 + 1)**2
        else:
            if quick:
                x0 = (T/Tc)**0.5
                x1 = x0 - 1.
                x2 = x1/x0
                x3 = S2*x2
                x4 = S1*x1 + x3 - 1.
                x5 = S1*x0
                x6 = S2 - x3 + x5
                x7 = 3.*S2
                a_alpha = a*x4*x4
                da_alpha_dT = a*x4*x6/T
                d2a_alpha_dT2 = a*(-x4*(-x2*x7 + x5 + x7) + x6*x6)/(2.*T*T)
            else:
                a_alpha = a*(S1*(-sqrt(T/Tc) + 1) + S2*(-sqrt(T/Tc) + 1)/sqrt(T/Tc) + 1)**2
                da_alpha_dT = a*((S1*(-sqrt(T/Tc) + 1) + S2*(-sqrt(T/Tc) + 1)/sqrt(T/Tc) + 1)*(-S1*sqrt(T/Tc)/T - S2/T - S2*(-sqrt(T/Tc) + 1)/(T*sqrt(T/Tc))))
                d2a_alpha_dT2 = a*(((S1*sqrt(T/Tc) + S2 - S2*(sqrt(T/Tc) - 1)/sqrt(T/Tc))**2 - (S1*sqrt(T/Tc) + 3*S2 - 3*S2*(sqrt(T/Tc) - 1)/sqrt(T/Tc))*(S1*(sqrt(T/Tc) - 1) + S2*(sqrt(T/Tc) - 1)/sqrt(T/Tc) - 1))/(2*T**2))
            return a_alpha, da_alpha_dT, d2a_alpha_dT2