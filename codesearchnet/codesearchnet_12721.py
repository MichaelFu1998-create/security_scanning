def to_dataframe(
            self,
            columns=BindingPrediction.fields + ("length",)):
        """
        Converts collection of BindingPrediction objects to DataFrame
        """
        return pd.DataFrame.from_records(
            [tuple([getattr(x, name) for name in columns]) for x in self],
            columns=columns)