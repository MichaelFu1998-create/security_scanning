def _validate_search_query(self, returning_query):
        """
        Checks to see that the query will not exceed the max query depth

        :param returning_query: The PIF system or Dataset query to execute.
        :type returning_query: :class:`PifSystemReturningQuery` or :class: `DatasetReturningQuery`
        """

        start_index = returning_query.from_index or 0
        size = returning_query.size or 0

        if start_index < 0:
            raise CitrinationClientError(
                "start_index cannot be negative. Please enter a value greater than or equal to zero")
        if size < 0:
            raise CitrinationClientError("Size cannot be negative. Please enter a value greater than or equal to zero")
        if start_index + size > MAX_QUERY_DEPTH:
            raise CitrinationClientError(
                "Citrination does not support pagination past the {0}th result. Please reduce either the from_index and/or size such that their sum is below {0}".format(
                    MAX_QUERY_DEPTH))