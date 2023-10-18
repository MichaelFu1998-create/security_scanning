def setup_a_alpha_and_derivatives(self, i, T=None):
        r'''Sets `a`, `kappa`, `kappa0`, `kappa1`, `kappa2`, `kappa3` and `Tc`
        for a specific component before the 
        pure-species EOS's `a_alpha_and_derivatives` method is called. Both are 
        called by `GCEOSMIX.a_alpha_and_derivatives` for every component.'''
        if not hasattr(self, 'kappas'):
            self.kappas = []
            for Tc, kappa0, kappa1, kappa2, kappa3 in zip(self.Tcs, self.kappa0s, self.kappa1s, self.kappa2s, self.kappa3s):
                Tr = T/Tc
                kappa = kappa0 + ((kappa1 + kappa2*(kappa3 - Tr)*(1. - Tr**0.5))*(1. + Tr**0.5)*(0.7 - Tr))
                self.kappas.append(kappa)

        (self.a, self.kappa, self.kappa0, self.kappa1, self.kappa2, 
         self.kappa3, self.Tc) = (self.ais[i], self.kappas[i], self.kappa0s[i],
         self.kappa1s[i], self.kappa2s[i], self.kappa3s[i], self.Tcs[i])