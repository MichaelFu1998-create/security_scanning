def predict_proba(self, x, y=None, **kwargs):
        """ Predict the causal score using a trained RCC model

        Args:
            x (numpy.array or pandas.DataFrame or pandas.Series): First variable or dataset.
            args (numpy.array): second variable (optional depending on the 1st argument).

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        if self.clf is None:
            raise ValueError("Model has to be trained before making predictions.")
        if x is pandas.Series:
            input_ = self.featurize_row(x.iloc[0], x.iloc[1]).reshape((1, -1))
        elif x is pandas.DataFrame:
            input_ = np.array([self.featurize_row(x.iloc[0], x.iloc[1]) for row in x])
        elif y is not None:
            input_ = self.featurize_row(x, y).reshape((1, -1))
        else:
            raise TypeError("DataType not understood.")
        return self.clf.predict(input_)