def predict(self, X):
        """Reaction is considered belonging to model’s AD
        if its reaction signature coincides with ones used in training set.

        Parameters
        ----------
        X : after read rdf file

        Returns
        -------
        self : array contains True (reaction in AD) and False (reaction residing outside AD).
        """
        check_is_fitted(self, ['_train_signatures'])
        X = iter2array(X, dtype=ReactionContainer)
        return array([self.__get_signature(x) in self._train_signatures for x in X])