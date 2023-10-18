def run_feature_selection(self, df_data, target, idx=0, **kwargs):
        """Run feature selection for one node: wrapper around
        ``self.predict_features``.

        Args:
            df_data (pandas.DataFrame): All the observational data
            target (str): Name of the target variable
            idx (int): (optional) For printing purposes

        Returns:
            list: scores of each feature relatively to the target
        """
        list_features = list(df_data.columns.values)
        list_features.remove(target)
        df_target = pd.DataFrame(df_data[target], columns=[target])
        df_features = df_data[list_features]

        return self.predict_features(df_features, df_target, idx=idx, **kwargs)