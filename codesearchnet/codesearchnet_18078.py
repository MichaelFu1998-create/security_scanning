def _grad_one_param(self, funct, p, dl=2e-5, rts=False, nout=1, **kwargs):
        """
        Gradient of `func` wrt a single parameter `p`. (see _graddoc)
        """
        vals = self.get_values(p)
        f0 = funct(**kwargs)

        self.update(p, vals+dl)
        f1 = funct(**kwargs)

        if rts:
            self.update(p, vals)
        if nout == 1:
            return (f1 - f0) / dl
        else:
            return [(f1[i] - f0[i]) / dl for i in range(nout)]