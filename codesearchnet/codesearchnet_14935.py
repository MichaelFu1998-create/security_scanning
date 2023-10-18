def predict_proba(self, X):
        """Predict the distances for X to center of the training set.

        Parameters
        ----------
        X : array-like or sparse matrix, shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.

        Returns
        -------
        leverages: array of shape = [n_samples]
                   The objects distances to center of the training set.
        """
        # Check is fit had been called
        check_is_fitted(self, ['inverse_influence_matrix'])
        # Check that X have correct shape
        X = check_array(X)
        return self.__find_leverages(X, self.inverse_influence_matrix)