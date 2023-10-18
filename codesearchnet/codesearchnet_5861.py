def create(self, list_id, data):
        """
        Create a new webhook for a specific list.

        The documentation does not include any required request body
        parameters but the url parameter is being listed here as a required
        parameter in documentation and error-checking based on the description
        of the method

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "url": string*
        }
        """
        self.list_id = list_id
        if 'url' not in data:
            raise KeyError('The list webhook must have a url')
        check_url(data['url'])
        response = self._mc_client._post(url=self._build_path(list_id, 'webhooks'), data=data)
        if response is not None:
            self.webhook_id = response['id']
        else:
            self.webhook_id = None
        return response