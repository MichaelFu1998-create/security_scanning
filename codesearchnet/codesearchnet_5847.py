def create(self, data):
        """
        Retrieve OAuth2-based credentials to associate API calls with your
        application.

        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "client_id": string*,
            "client_secret": string*
        }
        """
        self.app_id = None
        if 'client_id' not in data:
            raise KeyError('The authorized app must have a client_id')
        if 'client_secret' not in data:
            raise KeyError('The authorized app must have a client_secret')
        return self._mc_client._post(url=self._build_path(), data=data)