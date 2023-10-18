async def set_typing(self, typing=hangouts_pb2.TYPING_TYPE_STARTED):
        """Set your typing status in this conversation.

        Args:
            typing: (optional) ``TYPING_TYPE_STARTED``, ``TYPING_TYPE_PAUSED``,
                or ``TYPING_TYPE_STOPPED`` to start, pause, or stop typing,
                respectively. Defaults to ``TYPING_TYPE_STARTED``.

        Raises:
            .NetworkError: If typing status cannot be set.
        """
        # TODO: Add rate-limiting to avoid unnecessary requests.
        try:
            await self._client.set_typing(
                hangouts_pb2.SetTypingRequest(
                    request_header=self._client.get_request_header(),
                    conversation_id=hangouts_pb2.ConversationId(id=self.id_),
                    type=typing,
                )
            )
        except exceptions.NetworkError as e:
            logger.warning('Failed to set typing status: {}'.format(e))
            raise