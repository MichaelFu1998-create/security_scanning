def a_alpha_and_derivatives(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives for this EOS. Returns `a_alpha`, `da_alpha_dT`, and 
        `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Uses the set values of `a`.
        
        .. math::
            a\alpha = a
        
            \frac{d a\alpha}{dT} = 0

            \frac{d^2 a\alpha}{dT^2} = 0
        '''
        if not full:
            return self.a
        else:
            a_alpha = self.a
            da_alpha_dT = 0.0
            d2a_alpha_dT2 = 0.0
            return a_alpha, da_alpha_dT, d2a_alpha_dT2