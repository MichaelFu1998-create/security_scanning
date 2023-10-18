def get_community_children(self, community_id, token=None):
        """
        Get the non-recursive children of the passed in community_id.

        :param community_id: The id of the requested community.
        :type community_id: int | long
        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :returns: List of the folders in the community.
        :rtype: dict[string, list]
        """
        parameters = dict()
        parameters['id'] = community_id
        if token:
            parameters['token'] = token
        response = self.request('midas.community.children', parameters)
        return response