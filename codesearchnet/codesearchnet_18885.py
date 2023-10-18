def list_communities(self, token=None):
        """
        List all communities visible to a user.

        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :returns: The list of communities.
        :rtype: list[dict]
        """
        parameters = dict()
        if token:
            parameters['token'] = token
        response = self.request('midas.community.list', parameters)
        return response