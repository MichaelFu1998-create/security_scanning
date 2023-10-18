def predict(self, X):
        """Predict if a particular sample is an outlier or not.

        Parameters
        ----------
         X : array-like or sparse matrix, shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.

        Returns
        -------
        y : array, shape (n_samples,)
            For each observations, tells whether or not (True or False) it should
            be considered as an inlier according to the fitted model.
        """
        # Check is fit had been called
        check_is_fitted(self, ['tree'])
        # Check data
        X = check_array(X)
        return self.tree.query(X)[0].flatten() <= self.threshold_value