def fit(self, X, y=None):
        '''
        Specify the data to which kernel values should be computed.

        Parameters
        ----------
        X : list of arrays or :class:`skl_groups.features.Features`
            The bags to compute "to".
        '''
        self.features_ = as_features(X, stack=True, bare=True)
        # TODO: could precompute things like squared norms if kernel == "rbf".
        # Probably should add support to sklearn instead of hacking it here.
        return self