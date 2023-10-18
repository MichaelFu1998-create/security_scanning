def setup_a_alpha_and_derivatives(self, i, T=None):
        r'''Sets `a`, `kappa`, and `Tc` for a specific component before the 
        pure-species EOS's `a_alpha_and_derivatives` method is called. Both are 
        called by `GCEOSMIX.a_alpha_and_derivatives` for every component.'''
        self.a, self.kappa, self.Tc = self.ais[i], self.kappas[i], self.Tcs[i]