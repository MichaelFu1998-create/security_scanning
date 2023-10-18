def transform(self, X):
        '''
        Compute kernels from X to :attr:`features_`.

        Parameters
        ----------
        X : list of arrays or :class:`skl_groups.features.Features`
            The bags to compute "from". Must have same dimension as
            :attr:`features_`.

        Returns
        -------
        K : array of shape ``[len(X), len(features_)]``
            The kernel evaluations from X to :attr:`features_`.
        '''

        X = as_features(X, stack=True, bare=True)
        Y = self.features_

        if X.dim != Y.dim:
            raise ValueError("MMK transform got dimension {} but had {} at fit"
                             .format(X.dim, Y.dim))

        pointwise = pairwise_kernels(X.stacked_features, Y.stacked_features,
                                     metric=self.kernel,
                                     filter_params=True,
                                     **self._get_kernel_params())

        # TODO: is there a way to do this without a Python loop?
        K = np.empty((len(X), len(Y)))
        for i in range(len(X)):
            for j in range(len(Y)):
                K[i, j] = pointwise[X._boundaries[i]:X._boundaries[i+1],
                                    Y._boundaries[j]:Y._boundaries[j+1]].mean()

        return K