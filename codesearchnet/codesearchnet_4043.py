def predict_features(self, df_features, df_target, idx=0, C=.1, **kwargs):
        """For one variable, predict its neighbouring nodes.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            idx (int): (optional) for printing purposes
            kwargs (dict): additional options for algorithms
            C (float): Penalty parameter of the error term

        Returns:
            list: scores of each feature relatively to the target
        """
        lsvc = LinearSVR(C=C).fit(df_features.values, df_target.values)

        return np.abs(lsvc.coef_)