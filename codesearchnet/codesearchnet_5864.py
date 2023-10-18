def delete(self, list_id, webhook_id):
        """
        Delete a specific webhook in a list.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param webhook_id: The unique id for the webhook.
        :type webhook_id: :py:class:`str`
        """
        self.list_id = list_id
        self.webhook_id = webhook_id
        return self._mc_client._delete(url=self._build_path(list_id, 'webhooks', webhook_id))