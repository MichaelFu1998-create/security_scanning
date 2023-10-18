def create(self, conversation_id, data):
        """
        Post a new message to a conversation.

        :param conversation_id: The unique id for the conversation.
        :type conversation_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "from_email": string*,
            "read": boolean*
        }
        """
        self.conversation_id = conversation_id
        if 'from_email' not in data:
            raise KeyError('The conversation message must have a from_email')
        check_email(data['from_email'])
        if 'read' not in data:
            raise KeyError('The conversation message must have a read')
        if data['read'] not in [True, False]:
            raise TypeError('The conversation message read must be True or False')
        response =  self._mc_client._post(url=self._build_path(conversation_id, 'messages'), data=data)
        if response is not None:
            self.message_id = response['id']
        else:
            self.message_id = None
        return response