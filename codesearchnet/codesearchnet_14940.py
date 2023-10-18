def fit(self, x, y=None):
        """Do nothing and return the estimator unchanged

        This method is just there to implement the usual API and hence work in pipelines.
        """
        if self._dtype is not None:
            iter2array(x, dtype=self._dtype)
        else:
            iter2array(x)
        return self