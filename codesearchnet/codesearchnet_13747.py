def add(self, foreign_currency, foreign_curve=None, fx_spot=1.0):
        """
        adds contents to FxShelf.
        If curve is FxCurve or FxDict, spot should turn curve.currency into self.currency,
        else spot should turn currency into self.currency by
        N in EUR * spot = N in USD for currency = EUR and self.currency = USD
        """
        assert isinstance(foreign_currency, type(self.currency))
        assert isinstance(foreign_curve, curve.RateCurve)
        assert isinstance(fx_spot, float)

        # create missing FxCurves
        self[self.currency, foreign_currency] = FxCurve.cast(fx_spot, self.domestic_curve, foreign_curve)
        self[foreign_currency, self.currency] = FxCurve.cast(1 / fx_spot, foreign_curve, self.domestic_curve)
        # update relevant FxCurves
        f = foreign_currency
        new = dict()
        for d, s in self:
            if s is self.currency and d is not foreign_currency:
                triangulated = self[d, s](self.domestic_curve.origin) * fx_spot
                if (d, f) in self:
                    self[d, f].foreign_curve = foreign_curve
                    self[d, f].fx_spot = triangulated
                    self[f, d].domestic_curve = foreign_curve
                    self[f, d].fx_spot = 1 / triangulated
                else:
                    new[d, f] = FxCurve.cast(triangulated, self[d, s].domestic_curve, foreign_curve)
                    new[f, d] = FxCurve.cast(1 / triangulated, foreign_curve, self[d, s].domestic_curve)
        self.update(new)