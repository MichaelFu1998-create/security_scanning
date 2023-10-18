def predict(self, X):
        """Predict inside or outside AD for X.

        Parameters
        ----------
        X : array-like or sparse matrix, shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.

        Returns
        -------
        ad : array of shape = [n_samples]
            Array contains True (reaction in AD) and False (reaction residing outside AD).
        """
        # Check is fit had been called
        check_is_fitted(self, ['inverse_influence_matrix'])
        # Check that X have correct shape
        X = check_array(X)
        return self.__find_leverages(X, self.inverse_influence_matrix) <= self.threshold_value