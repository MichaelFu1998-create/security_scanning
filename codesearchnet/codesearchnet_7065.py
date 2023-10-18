def setup_a_alpha_and_derivatives(self, i, T=None):
        r'''Sets `a`, `m`, and `Tc` for a specific component before the 
        pure-species EOS's `a_alpha_and_derivatives` method is called. Both are 
        called by `GCEOSMIX.a_alpha_and_derivatives` for every component.'''
        self.a, self.m, self.Tc = self.ais[i], self.ms[i], self.Tcs[i]