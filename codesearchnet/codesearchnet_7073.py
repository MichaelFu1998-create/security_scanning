def setup_a_alpha_and_derivatives(self, i, T=None):
        r'''Sets `a`, `S1`, `S2` and `Tc` for a specific component before the 
        pure-species EOS's `a_alpha_and_derivatives` method is called. Both are 
        called by `GCEOSMIX.a_alpha_and_derivatives` for every component.'''
        self.a, self.Tc, self.S1, self.S2  = self.ais[i], self.Tcs[i], self.S1s[i], self.S2s[i]