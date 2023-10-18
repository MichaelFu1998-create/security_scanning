def predict(self, X):
        """ Predict if a particular sample is an outlier or not.

        Parameters
        ----------
        X : array-like or sparse matrix, shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.

        Returns
        -------
        is_inlier : array, shape (n_samples,)
                   For each observations, tells whether or not (True or False) it should
                   be considered as an inlier according to the fitted model.
        """
        # Check is fit had been called
        check_is_fitted(self, ['_x_min', '_x_max'])

        # Input validation
        X = check_array(X)
        return ((X - self._x_min).min(axis=1) >= 0) & ((self._x_max - X).min(axis=1) >= 0)