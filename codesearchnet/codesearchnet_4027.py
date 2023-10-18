def predict_dataset(self, df):
        """Runs Jarfo independently on all pairs.

        Args:
            x (pandas.DataFrame): a CEPC format Dataframe.
            kwargs (dict): additional arguments for the algorithms

        Returns:
            pandas.DataFrame: a Dataframe with the predictions.
        """
        if len(list(df.columns)) == 2:
            df.columns = ["A", "B"]
        if self.model is None:
            raise AssertionError("Model has not been trained before predictions")
        df2 = DataFrame()

        for idx, row in df.iterrows():
            df2 = df2.append(row, ignore_index=True)
            df2 = df2.append({'A': row["B"], 'B': row["A"]}, ignore_index=True)
        return predict.predict(deepcopy(df2), deepcopy(self.model))[::2]