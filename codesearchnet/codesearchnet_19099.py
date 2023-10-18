def fit(self, X, y=None):
        '''
        Picks the elements of the basis to use for the given data.

        Only depends on the dimension of X. If it's more convenient, you can
        pass a single integer for X, which is the dimension to use.

        Parameters
        ----------
        X : an integer, a :class:`Features` instance, or a list of bag features
            The input data, or just its dimension, since only the dimension is
            needed here.
        '''
        if is_integer(X):
            dim = X
        else:
            X = as_features(X)
            dim = X.dim
        M = self.smoothness

        # figure out the smooth-enough elements of our basis
        inds = np.mgrid[(slice(M + 1),) * dim].reshape(dim, (M + 1) ** dim).T
        self.inds_ = inds[(inds ** 2).sum(axis=1) <= M ** 2]
        return self