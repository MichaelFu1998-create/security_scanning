def solr_advanced_search(self, query, token=None, limit=20):
        """
        Search item metadata using Apache Solr.

        :param query: The Apache Lucene search query.
        :type query: string
        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :param limit: (optional) The limit of the search.
        :type limit: int | long
        :returns: The list of items that match the search query.
        :rtype: list[dict]
        """
        parameters = dict()
        parameters['query'] = query
        parameters['limit'] = limit
        if token:
            parameters['token'] = token
        response = self.request('midas.solr.search.advanced', parameters)
        return response