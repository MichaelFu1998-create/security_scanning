def cleanup_a_alpha_and_derivatives(self):
        r'''Removes properties set by `setup_a_alpha_and_derivatives`; run by
        `GCEOSMIX.a_alpha_and_derivatives` after `a_alpha` is calculated for 
        every component'''
        del(self.a, self.kappa, self.kappa0, self.kappa1, self.Tc)