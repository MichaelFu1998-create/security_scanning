def get_community_by_name(self, name, token=None):
        """
        Get a community based on its name.

        :param name: The name of the target community.
        :type name: string
        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :returns: The requested community.
        :rtype: dict
        """
        parameters = dict()
        parameters['name'] = name
        if token:
            parameters['token'] = token
        response = self.request('midas.community.get', parameters)
        return response