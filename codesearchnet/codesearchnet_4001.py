def predict_features(self, df_features, df_target, idx=0, **kwargs):
        """For one variable, predict its neighbouring nodes.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            idx (int): (optional) for printing purposes
            kwargs (dict): additional options for algorithms

        Returns:
            list: scores of each feature relatively to the target

        .. warning::
           Not implemented. Implemented by the algorithms.
        """

        y = np.transpose(df_target.values)
        X = np.transpose(df_features.values)

        path, beta, A, lam = hsiclasso(X, y)

        return beta