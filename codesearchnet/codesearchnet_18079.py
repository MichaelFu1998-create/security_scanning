def _hess_two_param(self, funct, p0, p1, dl=2e-5, rts=False, **kwargs):
        """
        Hessian of `func` wrt two parameters `p0` and `p1`. (see _graddoc)
        """
        vals0 = self.get_values(p0)
        vals1 = self.get_values(p1)

        f00 = funct(**kwargs)

        self.update(p0, vals0+dl)
        f10 = funct(**kwargs)

        self.update(p1, vals1+dl)
        f11 = funct(**kwargs)

        self.update(p0, vals0)
        f01 = funct(**kwargs)

        if rts:
            self.update(p0, vals0)
            self.update(p1, vals1)
        return (f11 - f10 - f01 + f00) / (dl**2)