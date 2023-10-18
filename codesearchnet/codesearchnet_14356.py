def train(cls, new_data, old=None):
        """
        Train a continuous scale

        Parameters
        ----------
        new_data : array_like
            New values
        old : array_like
            Old range. Most likely a tuple of length 2.

        Returns
        -------
        out : tuple
            Limits(range) of the scale
        """
        if not len(new_data):
            return old

        if not hasattr(new_data, 'dtype'):
            new_data = np.asarray(new_data)

        if new_data.dtype.kind not in CONTINUOUS_KINDS:
            raise TypeError(
                "Discrete value supplied to continuous scale")

        if old is not None:
            new_data = np.hstack([new_data, old])

        return min_max(new_data, na_rm=True, finite=True)