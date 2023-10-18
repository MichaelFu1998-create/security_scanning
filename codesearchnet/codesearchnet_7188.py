async def _handle_set_typing_notification(self, set_typing_notification):
        """Receive SetTypingNotification and update the conversation.

        Args:
            set_typing_notification: hangouts_pb2.SetTypingNotification
                instance
        """
        conv_id = set_typing_notification.conversation_id.id
        res = parsers.parse_typing_status_message(set_typing_notification)
        await self.on_typing.fire(res)
        try:
            conv = await self._get_or_fetch_conversation(conv_id)
        except exceptions.NetworkError:
            logger.warning(
                'Failed to fetch conversation for typing notification: %s',
                conv_id
            )
        else:
            await conv.on_typing.fire(res)