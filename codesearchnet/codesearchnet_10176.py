def pif_search(self, pif_system_returning_query):
        """
        Run a PIF query against Citrination.

        :param pif_system_returning_query: The PIF system query to execute.
        :type pif_system_returning_query: :class:`PifSystemReturningQuery`
        :return: :class:`PifSearchResult` object with the results of the query.
        :rtype: :class:`PifSearchResult`
        """

        self._validate_search_query(pif_system_returning_query)
        return self._execute_search_query(
            pif_system_returning_query,
            PifSearchResult
        )