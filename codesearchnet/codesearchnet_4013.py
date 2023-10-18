def predict_dataset(self, x, **kwargs):
        """Generic dataset prediction function.

        Runs the score independently on all pairs.

        Args:
            x (pandas.DataFrame): a CEPC format Dataframe.
            kwargs (dict): additional arguments for the algorithms

        Returns:
            pandas.DataFrame: a Dataframe with the predictions.
        """
        printout = kwargs.get("printout", None)
        pred = []
        res = []
        x.columns = ["A", "B"]
        for idx, row in x.iterrows():
            a = scale(row['A'].reshape((len(row['A']), 1)))
            b = scale(row['B'].reshape((len(row['B']), 1)))

            pred.append(self.predict_proba(a, b, idx=idx))

            if printout is not None:
                res.append([row['SampleID'], pred[-1]])
                DataFrame(res, columns=['SampleID', 'Predictions']).to_csv(
                    printout, index=False)
        return pred