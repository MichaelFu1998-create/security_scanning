def train(cls, new_data, old=None, drop=False, na_rm=False):
        """
        Train a continuous scale

        Parameters
        ----------
        new_data : array_like
            New values
        old : array_like
            Old range. List of values known to the scale.
        drop : bool
            Whether to drop(not include) unused categories
        na_rm : bool
            If ``True``, remove missing values. Missing values
            are either ``NaN`` or ``None``.

        Returns
        -------
        out : list
            Values covered by the scale
        """
        if not len(new_data):
            return old

        if old is None:
            old = []

        # Get the missing values (NaN & Nones) locations and remove them
        nan_bool_idx = pd.isnull(new_data)
        has_na = np.any(nan_bool_idx)
        if not hasattr(new_data, 'dtype'):
            new_data = np.asarray(new_data)
        new_data = new_data[~nan_bool_idx]

        if new_data.dtype.kind not in DISCRETE_KINDS:
            raise TypeError(
                "Continuous value supplied to discrete scale")

        # Train i.e. get the new values
        if pdtypes.is_categorical_dtype(new_data):
            try:
                new = list(new_data.cat.categories)  # series
            except AttributeError:
                new = list(new_data.categories)      # plain categorical
            if drop:
                present = set(new_data.drop_duplicates())
                new = [i for i in new if i in present]
        else:
            try:
                new = np.unique(new_data)
                new.sort()
            except TypeError:
                # new_data probably has nans and other types
                new = list(set(new_data))
                new = multitype_sort(new)

        # Add nan if required
        if has_na and not na_rm:
            new = np.hstack([new, np.nan])

        # update old
        old_set = set(old)
        return list(old) + [i for i in new if (i not in old_set)]