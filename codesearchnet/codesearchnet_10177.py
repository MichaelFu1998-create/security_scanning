def dataset_search(self, dataset_returning_query):
        """
        Run a dataset query against Citrination.

        :param dataset_returning_query: :class:`DatasetReturningQuery` to execute.
        :type dataset_returning_query: :class:`DatasetReturningQuery`
        :return: Dataset search result object with the results of the query.
        :rtype: :class:`DatasetSearchResult`
        """

        self._validate_search_query(dataset_returning_query)
        return self._execute_search_query(
            dataset_returning_query,
            DatasetSearchResult
        )