async def set_conversation_notification_level(
            self, set_conversation_notification_level_request
    ):
        """Set the notification level of a conversation."""
        response = hangouts_pb2.SetConversationNotificationLevelResponse()
        await self._pb_request(
            'conversations/setconversationnotificationlevel',
            set_conversation_notification_level_request, response
        )
        return response