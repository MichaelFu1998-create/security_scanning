async def _get_or_fetch_conversation(self, conv_id):
        """Get a cached conversation or fetch a missing conversation.

        Args:
            conv_id: string, conversation identifier

        Raises:
            NetworkError: If the request to fetch the conversation fails.

        Returns:
            :class:`.Conversation` with matching ID.
        """
        conv = self._conv_dict.get(conv_id, None)
        if conv is None:
            logger.info('Fetching unknown conversation %s', conv_id)
            res = await self._client.get_conversation(
                hangouts_pb2.GetConversationRequest(
                    request_header=self._client.get_request_header(),
                    conversation_spec=hangouts_pb2.ConversationSpec(
                        conversation_id=hangouts_pb2.ConversationId(
                            id=conv_id
                        )
                    ), include_event=False
                )
            )
            conv_state = res.conversation_state
            event_cont_token = None
            if conv_state.HasField('event_continuation_token'):
                event_cont_token = conv_state.event_continuation_token
            return self._add_conversation(conv_state.conversation,
                                          event_cont_token=event_cont_token)
        else:
            return conv