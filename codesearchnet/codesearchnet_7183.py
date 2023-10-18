def _add_conversation(self, conversation, events=[],
                          event_cont_token=None):
        """Add new conversation from hangouts_pb2.Conversation"""
        # pylint: disable=dangerous-default-value
        conv_id = conversation.conversation_id.id
        logger.debug('Adding new conversation: {}'.format(conv_id))
        conv = Conversation(self._client, self._user_list, conversation,
                            events, event_cont_token)
        self._conv_dict[conv_id] = conv
        return conv