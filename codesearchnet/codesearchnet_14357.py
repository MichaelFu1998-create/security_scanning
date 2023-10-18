def map(cls, x, palette, limits, na_value=None, oob=censor):
        """
        Map values to a continuous palette

        Parameters
        ----------
        x : array_like
            Continuous values to scale
        palette : callable ``f(x)``
            palette to use
        na_value : object
            Value to use for missing values.
        oob : callable ``f(x)``
            Function to deal with values that are
            beyond the limits

        Returns
        -------
        out : array_like
            Values mapped onto a palette
        """
        x = oob(rescale(x, _from=limits))
        pal = palette(x)
        try:
            pal[pd.isnull(x)] = na_value
        except TypeError:
            pal = [v if not pd.isnull(v) else na_value for v in pal]

        return pal