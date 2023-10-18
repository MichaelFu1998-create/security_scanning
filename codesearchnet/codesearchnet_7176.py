async def set_notification_level(self, level):
        """Set the notification level of this conversation.

        Args:
            level: ``NOTIFICATION_LEVEL_QUIET`` to disable notifications, or
                ``NOTIFICATION_LEVEL_RING`` to enable them.

        Raises:
            .NetworkError: If the request fails.
        """
        await self._client.set_conversation_notification_level(
            hangouts_pb2.SetConversationNotificationLevelRequest(
                request_header=self._client.get_request_header(),
                conversation_id=hangouts_pb2.ConversationId(id=self.id_),
                level=level,
            )
        )