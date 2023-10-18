def setup_a_alpha_and_derivatives(self, i, T=None):
        r'''Sets `a`, `kappa0`, `kappa1`, and `Tc` for a specific component before the 
        pure-species EOS's `a_alpha_and_derivatives` method is called. Both are 
        called by `GCEOSMIX.a_alpha_and_derivatives` for every component.'''
        if not hasattr(self, 'kappas'):
            self.kappas = [kappa0 + kappa1*(1 + (T/Tc)**0.5)*(0.7 - (T/Tc)) for kappa0, kappa1, Tc in zip(self.kappa0s, self.kappa1s, self.Tcs)]
        self.a, self.kappa, self.kappa0, self.kappa1, self.Tc = self.ais[i], self.kappas[i], self.kappa0s[i], self.kappa1s[i], self.Tcs[i]