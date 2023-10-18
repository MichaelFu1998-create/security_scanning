def setup_a_alpha_and_derivatives(self, i, T=None):
        r'''Sets `a`, `omega`, and `Tc` for a specific component before the 
        pure-species EOS's `a_alpha_and_derivatives` method is called. Both are 
        called by `GCEOSMIX.a_alpha_and_derivatives` for every component.'''
        self.a, self.Tc, self.omega  = self.ais[i], self.Tcs[i], self.omegas[i]