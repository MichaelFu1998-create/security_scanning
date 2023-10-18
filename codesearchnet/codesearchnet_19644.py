def index_row(self, dataframe):
        """
        Indexes the row based on the request parameters.
        """
        return dataframe.loc[self.kwargs[self.lookup_url_kwarg]].to_frame().T