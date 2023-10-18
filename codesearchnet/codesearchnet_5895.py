def update(self, batch_webhook_id, data):
        """
        Update a webhook that will fire whenever any batch request completes
        processing.

        :param batch_webhook_id: The unique id for the batch webhook.
        :type batch_webhook_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "url": string*
        }
        """
        self.batch_webhook_id = batch_webhook_id
        if 'url' not in data:
            raise KeyError('The batch webhook must have a valid url')
        return self._mc_client._patch(url=self._build_path(batch_webhook_id), data=data)