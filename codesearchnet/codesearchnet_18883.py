def get_community_by_id(self, community_id, token=None):
        """
        Get a community based on its id.

        :param community_id: The id of the target community.
        :type community_id: int | long
        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :returns: The requested community.
        :rtype: dict
        """
        parameters = dict()
        parameters['id'] = community_id
        if token:
            parameters['token'] = token
        response = self.request('midas.community.get', parameters)
        return response