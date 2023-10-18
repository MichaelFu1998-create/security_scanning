def delete(self, batch_webhook_id):
        """
        Remove a batch webhook. Webhooks will no longer be sent to the given
        URL.

        :param batch_webhook_id: The unique id for the batch webhook.
        :type batch_webhook_id: :py:class:`str`
        """
        self.batch_webhook_id = batch_webhook_id
        return self._mc_client._delete(url=self._build_path(batch_webhook_id))