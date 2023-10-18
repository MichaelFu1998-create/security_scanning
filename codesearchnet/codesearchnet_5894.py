def get(self, batch_webhook_id, **queryparams):
        """
        Get information about a specific batch webhook.

        :param batch_webhook_id: The unique id for the batch webhook.
        :type batch_webhook_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.batch_webhook_id = batch_webhook_id
        return self._mc_client._get(url=self._build_path(batch_webhook_id), **queryparams)