def predict(self, X):
        """ In order to obtain the most likely label for a list of text

        Parameters
        ----------
        X : list of string
            Raw texts

        Returns
        -------
        C : list of string
            List labels
        """
        x = X
        if not isinstance(X, list):
            x = [X]
        y = self.estimator.predict(x)
        y = [item[0] for item in y]
        y = [self._remove_prefix(label) for label in y]
        if not isinstance(X, list):
            y = y[0]
        return y