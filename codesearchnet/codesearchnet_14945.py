def fit(self, X):
        """Fit structure-based AD. The training model  memorizes the unique set of reaction signature.

        Parameters
        ----------
        X : after read rdf file

        Returns
        -------
        self : object
        """
        X = iter2array(X, dtype=ReactionContainer)
        self._train_signatures = {self.__get_signature(x) for x in X}
        return self