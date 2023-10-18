def search(self, search, token=None):
        """
        Get the resources corresponding to a given query.

        :param search: The search criterion.
        :type search: string
        :param token: (optional) The credentials to use when searching.
        :type token: None | string
        :returns: Dictionary containing the search result. Notable is the
            dictionary item 'results', which is a list of item details.
        :rtype: dict
        """
        parameters = dict()
        parameters['search'] = search
        if token:
            parameters['token'] = token
        response = self.request('midas.resource.search', parameters)
        return response