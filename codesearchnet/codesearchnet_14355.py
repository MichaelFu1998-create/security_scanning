def apply(cls, x, palette, na_value=None, trans=None):
        """
        Scale data continuously

        Parameters
        ----------
        x : array_like
            Continuous values to scale
        palette : callable ``f(x)``
            Palette to use
        na_value : object
            Value to use for missing values.
        trans : trans
            How to transform the data before scaling. If
            ``None``, no transformation is done.

        Returns
        -------
        out : array_like
            Scaled values
        """
        if trans is not None:
            x = trans.transform(x)

        limits = cls.train(x)
        return cls.map(x, palette, limits, na_value)