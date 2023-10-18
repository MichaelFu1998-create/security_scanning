def map(cls, x, palette, limits, na_value=None):
        """
        Map values to a discrete palette

        Parameters
        ----------
        palette : callable ``f(x)``
            palette to use
        x : array_like
            Continuous values to scale
        na_value : object
            Value to use for missing values.

        Returns
        -------
        out : array_like
            Values mapped onto a palette
        """
        n = len(limits)
        pal = palette(n)[match(x, limits)]
        try:
            pal[pd.isnull(x)] = na_value
        except TypeError:
            pal = [v if not pd.isnull(v) else na_value for v in pal]

        return pal