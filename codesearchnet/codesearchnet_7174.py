async def leave(self):
        """Leave this conversation.

        Raises:
            .NetworkError: If conversation cannot be left.
        """
        is_group_conversation = (self._conversation.type ==
                                 hangouts_pb2.CONVERSATION_TYPE_GROUP)
        try:
            if is_group_conversation:
                await self._client.remove_user(
                    hangouts_pb2.RemoveUserRequest(
                        request_header=self._client.get_request_header(),
                        event_request_header=self._get_event_request_header(),
                    )
                )
            else:
                await self._client.delete_conversation(
                    hangouts_pb2.DeleteConversationRequest(
                        request_header=self._client.get_request_header(),
                        conversation_id=hangouts_pb2.ConversationId(
                            id=self.id_
                        ),
                        delete_upper_bound_timestamp=parsers.to_timestamp(
                            datetime.datetime.now(tz=datetime.timezone.utc)
                        )
                    )
                )
        except exceptions.NetworkError as e:
            logger.warning('Failed to leave conversation: {}'.format(e))
            raise