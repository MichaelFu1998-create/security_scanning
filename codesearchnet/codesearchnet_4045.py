def predict_features(self, df_features, df_target, idx=0, **kwargs):
        """For one variable, predict its neighbouring nodes.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            idx (int): (optional) for printing purposes
            kwargs (dict): additional options for algorithms

        Returns:
            list: scores of each feature relatively to the target
        """
        X = df_features.values
        y = df_target.values
        clf = ard(compute_score=True)
        clf.fit(X, y.ravel())

        return np.abs(clf.coef_)