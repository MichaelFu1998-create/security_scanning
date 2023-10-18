def paginate_dataframe(self, dataframe):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_dataframe(dataframe, self.request, view=self)