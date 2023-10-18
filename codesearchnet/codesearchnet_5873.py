def get(self, conversation_id, **queryparams):
        """
        Get details about an individual conversation.

        :param conversation_id: The unique id for the conversation.
        :type conversation_id: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.conversation_id = conversation_id
        return self._mc_client._get(url=self._build_path(conversation_id), **queryparams)