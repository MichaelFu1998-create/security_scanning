def get_dataframe(self):
        """
        Get the DataFrame for this view.
        Defaults to using `self.dataframe`.

        This method should always be used rather than accessing `self.dataframe`
        directly, as `self.dataframe` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        dataframes depending on the incoming request.
        """
        assert self.dataframe is not None, (
            "'%s' should either include a `dataframe` attribute, "
            "or override the `get_dataframe()` method."
            % self.__class__.__name__
        )

        dataframe = self.dataframe
        return dataframe