def list_users(self, limit=20):
        """
        List the public users in the system.

        :param limit: (optional) The number of users to fetch.
        :type limit: int | long
        :returns: The list of users.
        :rtype: list[dict]
        """
        parameters = dict()
        parameters['limit'] = limit
        response = self.request('midas.user.list', parameters)
        return response