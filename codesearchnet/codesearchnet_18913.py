def create_submission(self, token, **kwargs):
        """
        Associate a result item with a particular scalar value.

        :param token: A valid token for the user in question.
        :type token: string
        :param uuid (optional) The uuid of the submission (must be unique)
        :type uuid: string
        :param name (optional) The name of the submission
        :type name: string
        :returns: The submission object that was created.
        :rtype: dict
        """
        parameters = {}
        parameters['token'] = token
        optional_keys = ['uuid', 'name']
        for key in optional_keys:
            if key in kwargs:
                parameters[key] = kwargs[key]
        return self.request('midas.tracker.submission.create', parameters)