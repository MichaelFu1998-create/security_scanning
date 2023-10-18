def create_community(self, token, name, **kwargs):
        """
        Create a new community or update an existing one using the uuid.

        :param token: A valid token for the user in question.
        :type token: string
        :param name: The community name.
        :type name: string
        :param description: (optional) The community description.
        :type description: string
        :param uuid: (optional) uuid of the community. If none is passed, will
            generate one.
        :type uuid: string
        :param privacy: (optional) Default 'Public', possible values
            [Public|Private].
        :type privacy: string
        :param can_join: (optional) Default 'Everyone', possible values
            [Everyone|Invitation].
        :type can_join: string
        :returns: The community dao that was created.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['name'] = name
        optional_keys = ['description', 'uuid', 'privacy', 'can_join']
        for key in optional_keys:
            if key in kwargs:
                if key == 'can_join':
                    parameters['canjoin'] = kwargs[key]
                    continue
                parameters[key] = kwargs[key]
        response = self.request('midas.community.create', parameters)
        return response