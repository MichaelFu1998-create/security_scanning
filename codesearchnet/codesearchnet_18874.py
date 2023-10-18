def login_with_api_key(self, email, api_key, application='Default'):
        """
        Login and get a token. If you do not specify a specific application,
        'Default' will be used.

        :param email: Email address of the user
        :type email: string
        :param api_key: API key assigned to the user
        :type api_key: string
        :param application: (optional) Application designated for this API key
        :type application: string
        :returns: Token to be used for interaction with the API until
            expiration
        :rtype: string
        """
        parameters = dict()
        parameters['email'] = BaseDriver.email = email  # Cache email
        parameters['apikey'] = BaseDriver.apikey = api_key  # Cache API key
        parameters['appname'] = application
        response = self.request('midas.login', parameters)
        if 'token' in response:  # normal case
            return response['token']
        if 'mfa_token_id':  # case with multi-factor authentication
            return response['mfa_token_id']