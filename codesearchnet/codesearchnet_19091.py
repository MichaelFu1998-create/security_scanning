def fit(self, X, y=None):
        '''
        If scale_by_median, find :attr:`median_`; otherwise, do nothing.

        Parameters
        ----------
        X : array
            The raw pairwise distances.
        '''

        X = check_array(X)
        if self.scale_by_median:
            self.median_ = np.median(X[np.triu_indices_from(X, k=1)],
                                     overwrite_input=True)
        elif hasattr(self, 'median_'):
            del self.median_
        return self