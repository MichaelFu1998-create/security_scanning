def a_alpha_and_derivatives(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives for this EOS. Returns `a_alpha`, `da_alpha_dT`, and 
        `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Uses the set values of `Tc`, `m`, and `a`.
        
        .. math::
            a\alpha = a \left(m \left(- \sqrt{\frac{T}{Tc}} + 1\right)
            + 1\right)^{2}
        
            \frac{d a\alpha}{dT} = \frac{a m}{T} \sqrt{\frac{T}{Tc}} \left(m
            \left(\sqrt{\frac{T}{Tc}} - 1\right) - 1\right)

            \frac{d^2 a\alpha}{dT^2} = \frac{a m \sqrt{\frac{T}{Tc}}}{2 T^{2}}
            \left(m + 1\right)
        '''
        a, Tc, m = self.a, self.Tc, self.m
        sqTr = (T/Tc)**0.5
        a_alpha = a*(m*(1. - sqTr) + 1.)**2
        if not full:
            return a_alpha
        else:
            da_alpha_dT = -a*m*sqTr*(m*(-sqTr + 1.) + 1.)/T
            d2a_alpha_dT2 =  a*m*sqTr*(m + 1.)/(2.*T*T)
            return a_alpha, da_alpha_dT, d2a_alpha_dT2