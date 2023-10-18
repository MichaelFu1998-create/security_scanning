def predict_proba(self, X):
        """Returns the value of the nearest neighbor from the training set.

        Parameters
        ----------
         X : array-like or sparse matrix, shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.

        Returns
        -------
        y : array, shape (n_samples,)
        """
        # Check is fit had been called
        check_is_fitted(self, ['tree'])
        # Check data
        X = check_array(X)
        return self.tree.query(X)[0].flatten()