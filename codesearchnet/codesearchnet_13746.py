def cast(cls, fx_spot, domestic_curve=None, foreign_curve=None):
        """
        creator method to build FxCurve

        :param float fx_spot: fx spot rate
        :param RateCurve domestic_curve: domestic discount curve
        :param RateCurve foreign_curve: foreign discount curve
        :return:
        """
        assert domestic_curve.origin == foreign_curve.origin
        return cls(fx_spot, domestic_curve=domestic_curve, foreign_curve=foreign_curve)