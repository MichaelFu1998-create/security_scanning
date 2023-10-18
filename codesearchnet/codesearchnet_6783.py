def a_alpha_and_derivatives(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives for this EOS. Returns `a_alpha`, `da_alpha_dT`, and 
        `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Uses the set values of `Tc`, `omega`, and `a`.
        
        Because of its similarity for the TWUPR EOS, this has been moved to an 
        external `TWU_a_alpha_common` function. See it for further 
        documentation.
        '''
        return TWU_a_alpha_common(T, self.Tc, self.omega, self.a, full=full, quick=quick, method='SRK')